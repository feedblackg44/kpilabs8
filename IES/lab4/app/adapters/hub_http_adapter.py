import datetime
import json
import logging

import requests as requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.hub_gateway import HubGateway


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat().replace(" ", "")
        return json.JSONEncoder.default(self, obj)


class HubHttpAdapter(HubGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_data: ProcessedAgentData):
        # Make a POST request to the Store API endpoint with the processed data
        response = requests.post(
            f"{self.api_base_url}/processed_agent_data/",
            data=json.dumps(processed_data.dict(), cls=DateTimeEncoder)
        )
        if response.status_code != 200:
            logging.error(f"Failed to save data to Store API, status code: {response.status_code}")
            return False
        else:
            logging.info("Data saved to Store API successfully")
            return True
