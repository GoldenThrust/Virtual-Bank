import os
import json
import requests
from django.test import TestCase
from api.virtual_bank.settings import API_URL
from debit_cards.models import DebitCard


class AccountTest(TestCase):
    def setUp(self):
        self.url = f"{API_URL}/api/v1/"
        self.main_url = f"{API_URL}/api/v1/accounts/"
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
        for data in self.json_data:
            url = f"{self.main_url}create/"
            response = requests.post(url, data=data, headers=self.headers[i])
            data = response.json()
            i += 1
            for key in data:
                self.assertIsNotNone(data[key])

    def test_list_accounts(self):
        url = f"{self.main_url}lists/"
        for header in self.headers:
            response = requests.get(url, headers=header)
            self.assertEqual(response.status_code, 200)
            accounts = response.json()
            for account in accounts:
                if account["account_type"] == "CURRENT":
                    try:
                        DebitCard.objects.filter(account=account["id"])
                    except DebitCard.DoesNotExist:
                        self.fail("Debit card does not exist")

            self.assertGreater(len(account), 0)
