import os
import json
import requests
from django.test import TestCase
from django.test import LiveServerTestCase

class CustomLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server_host = cls.live_server_url.split('://')[1].split(':')[0]
        cls.server_port = cls.live_server_url.split(':')[2]

    @classmethod
    def get_server_info(cls):
        return cls.server_host, cls.server_port



class AccountTest(TestCase, CustomLiveServerTestCase):
    def setUp(self):
        self.host, self.port = self.get_server_info()
        self.url = "http://localhost:8000/api/v1/"
        self.main_url = "http://localhost:8000/api/v1/users/"
        self.headers = {"Authorization": "Basic dXNlcl8xMjM6cGFzczEyMzQ="}

        # Path to your JSON file containing test data
        file_path = os.path.join("..", "json", "users.json")
        print(file_path)
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