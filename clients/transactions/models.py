from django.db import models
from accounts.models import Account
import uuid

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
        ('DEBIT_CARD', 'Debit Card'),
    ]

    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("GBP", "GBP"),
        ("NGN", "NGN"),
        ("JPY", "JPY"),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    payer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payer')
    payee = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payee')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default="DEPOSIT")
    amount_sent = models.DecimalField(max_digits=15, decimal_places=2)
    amount_received = models.DecimalField(max_digits=15, decimal_places=2)
    currency_sent = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    currency_received = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    description = models.TextField(blank=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction ID: {self.pk} - Type: {self.get_transaction_type_display()} - Amount: {self.amount_received}"
