from django.db import models
from users.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [
        ("SAVINGS", "Savings"),
        ("CREDIT_CARD", "Credit Card"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default="SAVINGS")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    number = models.IntegerField(unique=True)
    currency = models.CharField(max_length=3, choices=[("USD", "USD"), ("EUR", "EUR"), ("GBP", "GBP"), ("NGN", "NGN")])
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_account_type_display()} - {self.number} - User: {self.user.username}"
