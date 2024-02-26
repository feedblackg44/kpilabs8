import json
from datetime import datetime
from typing import Set, List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from starlette.websockets import WebSocket, WebSocketDisconnect

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

DATABASE_URL = (f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"
                f"{POSTGRES_DB}")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("road_state", String),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime),
)


class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator('timestamp', mode='before')
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError("Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).")


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData


# Database model
class ProcessedAgentDataInDB(BaseModel):
    id: int
    road_state: str
    x: float
    y: float
    z: float
    latitude: float
    longitude: float
    timestamp: datetime


# FastAPI app setup
app = FastAPI()

# WebSocket subscriptions
subscriptions: Set[WebSocket] = set()


# FastAPI WebSocket endpoint
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)


# Function to send data to subscribed users
async def send_data_to_subscribers(data):
    for websocket in subscriptions:
        await websocket.send_json(json.dumps(data))


# FastAPI CRUDL endpoints

@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    insert_data = [
        {
            "road_state": item.road_state,
            "x": item.agent_data.accelerometer.x,
            "y": item.agent_data.accelerometer.y,
            "z": item.agent_data.accelerometer.z,
            "latitude": item.agent_data.gps.latitude,
            "longitude": item.agent_data.gps.longitude,
            "timestamp": item.agent_data.timestamp
        } for item in data
    ]

    with engine.begin() as conn:
        conn.execute(processed_agent_data.insert(), insert_data)

    await send_data_to_subscribers(insert_data)

    return {"message": "Data inserted successfully"}


@app.get("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int):
    with engine.connect() as conn:
        query = processed_agent_data.select().where(processed_agent_data.c.id == processed_agent_data_id)
        result = conn.execute(query).first()

        if not result:
            raise HTTPException(status_code=404,
                                detail=f"ProcessedAgentData with ID {processed_agent_data_id} not found")

        return result


@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def list_processed_agent_data():
    with engine.connect() as conn:
        query = processed_agent_data.select()
        results = conn.execute(query).fetchall()

        return results


@app.put("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def update_processed_agent_data(processed_agent_data_id: int, update_data: ProcessedAgentData):
    with engine.connect() as conn:
        select_query = processed_agent_data.select().where(processed_agent_data.c.id == processed_agent_data_id)
        existing_record = conn.execute(select_query).first()
        if not existing_record:
            raise HTTPException(status_code=404,
                                detail=f"ProcessedAgentData with ID {processed_agent_data_id} not found")

        update_values = {
            "road_state": update_data.road_state,
            "x": update_data.agent_data.accelerometer.x,
            "y": update_data.agent_data.accelerometer.y,
            "z": update_data.agent_data.accelerometer.z,
            "latitude": update_data.agent_data.gps.latitude,
            "longitude": update_data.agent_data.gps.longitude,
            "timestamp": update_data.agent_data.timestamp,
        }

        update_query = processed_agent_data.update().where(
            processed_agent_data.c.id == processed_agent_data_id
        ).values(**update_values)
        conn.execute(update_query)
        conn.commit()

        updated_record = conn.execute(select_query).first()
        return updated_record


@app.delete("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int):
    with engine.connect() as conn:
        select_query = processed_agent_data.select().where(processed_agent_data.c.id == processed_agent_data_id)
        record_to_delete = conn.execute(select_query).first()

        if not record_to_delete:
            raise HTTPException(status_code=404,
                                detail=f"ProcessedAgentData with ID {processed_agent_data_id} not found")

        delete_query = processed_agent_data.delete().where(processed_agent_data.c.id == processed_agent_data_id)
        conn.execute(delete_query)
        conn.commit()

        return record_to_delete


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
