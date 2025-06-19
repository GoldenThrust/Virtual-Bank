import os
import json
import requests
from django.test import TestCase
from django.urls import reverse

from api.virtual_bank.settings import API_URL


class UserTest(TestCase):
    def setUp(self):
        self.url =  API_URL

        # Path to your JSON file containing test data
        file_path = os.path.join("..", "json", "users.json")
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    def test_create_users(self):
        url = reverse('api:user_registration')
        
        for data in self.json_data:
            response = requests.post(f'{self.url}{url}', data=data)
            data = response.json()
            if not isinstance(data['username'], list) and not isinstance(data['email'], list) :
                self.assertEqual(response.status_code, 201)
                for key in data:
                    self.assertIsNotNone(data[key])