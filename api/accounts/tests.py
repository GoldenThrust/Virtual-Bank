import os
import json
import requests
from django.test import TestCase, Client
from debit_cards.models import DebitCard
from django.urls import reverse


class AccountTest(TestCase):
    def setUp(self):
        self.headers = [
            {"Authorization": "Basic dXNlcl8xMjM6cGFzczEyMzQ="},
            {"Authorization": "Basic amFuZV9kb2U6amFuZWRvZTE="},
            {"Authorization": "Basic c2FyYV9qb2huc29uOnNhcmFqNDU2"},
            {"Authorization": "Basic amRvZTpqZG9lMTIzNA=="},
            {"Authorization": "Basic ZW1pbHlfd2hpdGU6ZW1pbHkxMjM="},
            {"Authorization": "Basic amFzb25fZ3JlZW46amFzb25nMTIz"},
            {"Authorization": "Basic YW5uYV9icm93bjphbm5hYjc4OQ=="},
            {"Authorization": "Basic bWF4X21pbGxlcjptYXhtMTIzNA=="},
            {"Authorization": "Basic bGlzYV93aWxzb246bGlzYXcxMjM="},
            {"Authorization": "Basic bGlzYV93aWxzb246bGlzYXcxMjM="}
        ]

        # Path to your JSON file containing test data
        file_path = os.path.join("..", "json", "accounts.json")
        with open(file_path, "r") as f:
            self.json_data = json.load(f)

    def test_create_accounts(self):
        i = 0
        url = reverse('api:account_creation')
        for data in self.json_data:
            c = Client(headers=self.headers[i])
            response = c.post(url, data)
            data = response.json()
            i += 1
            for key in data:
                self.assertIsNotNone(data[key])