import logging
import os
import requests
from dataclasses import dataclass
from datetime import datetime
from requests.models import Response
from typing import Optional

logging.basicConfig(level=logging.INFO)

class APIClient:
    def __init__(self, base_url = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()

        

    def upload(self, file_path: str) -> Optional[str]:
        """Uploads a file to the server and returns the UID if successful."""
        url = f"{self.base_url}/upload"
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = self.session.post(url, files=files)
            if response.status_code == 200:
                return response.json().get('uid')
            else:
                logging.error(f"Failed to upload file")
                response.raise_for_status()

    def status(self, uid: str) -> Optional['Status']:
        """Fetches the status of an upload by UID."""
        url = f"{self.base_url}/status/{uid}"
        response = self.session.get(url)
        if response.status_code == 200:
            return Status.from_json(response.json())
        else:
            logging.error(f"Failed to get status for UID {uid}")
            response.raise_for_status()

@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    @staticmethod
    def from_json(data: dict) -> 'Status':
        """Creates a Status object from a JSON dictionary."""
        timestamp = datetime.strptime(data['timestamp'], "%Y%m%d%H%M%S")
        return Status(
            status=data['status'],
            filename=data['filename'],
            timestamp=timestamp,
            explanation=data.get('explanation')
        )
    
    def is_done(self) -> bool:
        """Checks if the status is 'done'."""
        return self.status.lower() == 'done'


