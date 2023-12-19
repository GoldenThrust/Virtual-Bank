import os
import json
import requests
from django.test import TestCase, Client
from django.urls import reverse

class UserTest(TestCase):
    def setUp(self):
        self.c = Client(headers={"Authorization": "Basic dXNlcl8xMjM6cGFzczEyMzQ="})

        # Path to your JSON file containing test data
        file_path = os.path.join("..", "json", "users.json")
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def test_create_users(self):
        c = Client()
        url = reverse('api:user_create')
        
        self.assertIsNotNone('hello')
        for data in self.json_data:
            response = c.post(url, data)
            data = response.json()
            print(response)
            if not isinstance(data['username'], list) and not isinstance(data['email'], list) :
                self.assertEqual(response.status_code, 201)
                for key in data:
                    self.assertIsNotNone(data[key])


    def test_list_users(self):
        url  = reverse('api:user_list')
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertGreater(len(users), 0)