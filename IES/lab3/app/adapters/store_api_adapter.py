import datetime
import json
import logging
from typing import List
import requests
from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_api_gateway import StoreGateway


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat().replace(" ", "")
        return json.JSONEncoder.default(self, obj)


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        # Make a POST request to the Store API endpoint with the processed data
        response = requests.post(
            f"{self.api_base_url}/processed_agent_data/",
            data=json.dumps([item.dict() for item in processed_agent_data_batch], cls=DateTimeEncoder)
        )
        if response.status_code != 200:
            logging.error(f"Failed to save data to Store API, status code: {response.status_code}")
            return False
        else:
            logging.info("Data saved to Store API successfully")
            return True
