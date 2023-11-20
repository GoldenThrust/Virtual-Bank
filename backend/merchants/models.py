from django.db import models
from users.models import User
from accounts.models import Account


class Merchant(models.Model):

    PAYMENT_METHODS = [
        ("DEPOSIT", "Deposit"),
        ("TRANSFER", "Transfer"),
        ("CREDIT_CARD", "Credit Card"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20)
    payment_methods_accepted = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    business_hours = models.JSONField()
    website_url = models.URLField(max_length=200)
    api_key = models.CharField(max_length=255, null=True)
    # public_key = models.TextField()
    # private_key = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Category: {self.category}"
