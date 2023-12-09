import os
import json
import requests
from django.test import TestCase


class UserTest(TestCase):
    def setUp(self):
        self.url = "http://localhost:8000/api/v1/"
        self.main_url = "http://localhost:8000/api/v1/users/"
        self.headers = {"Authorization": "Basic dXNlcl8xMjM6cGFzczEyMzQ="}

        # Path to your JSON file containing test data
        file_path = os.path.join("..", "json", "users.json")
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def test_create_users(self):
        for data in self.json_data:
            url  = f'{self.main_url}create/'
            response = requests.post(url, data=data)
            data = response.json()
            if not isinstance(data['username'], list) and not isinstance(data['email'], list) :
                self.assertEqual(response.status_code, 201)
                for key in data:
                    self.assertIsNotNone(data[key])

    def test_list_users(self):
        url  = f'{self.main_url}lists/'
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertGreater(len(users), 0)