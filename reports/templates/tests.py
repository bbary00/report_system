from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'


class TemplateTests(TestCase):
    """Class to test Template model response"""

    URI = reverse('template-list')

    def test_get_templates_failed(self):
        """Test to get all templates objects from db without auth"""
        url = BASE_URL + self.URI
        res = requests.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_templates(self):
        """Test to get all templates objects from db without auth"""
        url = BASE_URL + self.URI
        headers = {
            'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IklEXzMyOTljZTk5LTQyMjEtNDViZS1iYzA1LWJlZmFkNjQyNzkyYiIsImV4cCI6MTU3MzY1NjkyNH0.jW8JuspCLTPFgwGgGQRau2bO0uTz0yzo4rOSmdPBzMw"
        }
        res = requests.get(url, headers=headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_template(self):
        """Test post template object in db"""
        url = BASE_URL + self.URI
        data = {
            "label": "wget",
            "description": "A non-interactive network donwloader",
            "inputs": [
                "url", "options"
            ]
        }

        headers = {
            'content-type': 'application/json',
            'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IklEXzMyOTljZTk5LTQyMjEtNDViZS1iYzA1LWJlZmFkNjQyNzkyYiIsImV4cCI6MTU3MzY1NjkyNH0.jW8JuspCLTPFgwGgGQRau2bO0uTz0yzo4rOSmdPBzMw"
        }

        res = requests.post(url, json.dumps(data), headers=headers)
        res_get = requests.get(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res_get.json()), 1)


class UserTests(TestCase):
    """Class to test user auth"""

    URI_signup = '/signup/'
    URI_login = '/login/'

    def test_sign_up_and_login(self):
        """Test to sign up user"""
        url = BASE_URL + self.URI_signup
        data = {
            "email": "test_email@gmail.com",
            "password": "testpwd",
            "username": "TestUser"
        }
        res = requests.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["data"]["username"], data["username"])
        self.assertEqual(res.json()["data"]["email"], data["email"])

        url = BASE_URL + self.URI_login
        data = {
            "password": "testpwd",
            "username": "TestUser"
        }
        res = requests.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in res.json()["data"].keys())



