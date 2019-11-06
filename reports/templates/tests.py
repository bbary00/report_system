from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

class ToolTests(TestCase):
    """Class to test Tool model response"""

    URI = reverse('template-list')

    def test_get_tools(self):
        """Test to get all Tool objects from db"""
        url = BASE_URL + self.URI
        print(url)
        res = requests.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_tool(self):
        """Test post Tool object in db"""
        url = BASE_URL + self.URI
        data = {
            "label": "wget",
            "description": "A non-interactive network donwloader",
            "inputs": [
                {
                    "name": "url",
                    "value": "https://medium.com"
                },
                {
                    "name": "options",
                    "value": 123
                }
            ]
        }

        headers = {
            'content-type': 'application/json',
            'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6Ik9yZXN0IiwiZXhwIjoxNTcxNDk0Mzk0LCJlbWFpbCI6Im9yZXN0QGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNTcxNDk0MDk0fQ.bHTypX90DclMpgAWjeuZzfi-uwFlDkOChX4bQ3emjus"
        }

        res = requests.post(url, json.dumps(data), headers=headers)
        res_get = requests.get(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res_get.json()), 3)


