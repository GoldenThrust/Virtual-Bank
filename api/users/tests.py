import os
import json
import requests
from django.test import TestCase
from django.urls import reverse

class UserTest(TestCase):
    def setUp(self):
        self.url =  'http://localhost:8000'

        # Path to your JSON file containing test data
        file_path = os.path.join("..", "json", "users.json")
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def test_create_users(self):
        url = reverse('api:user_create')
        
        self.assertIsNotNone('hello')
        for data in self.json_data:
            response = requests.post(f'{self.url}{url}', data=data)
            data = response.json()
            if not isinstance(data['username'], list) and not isinstance(data['email'], list) :
                self.assertEqual(response.status_code, 201)
                for key in data:
                    self.assertIsNotNone(data[key])