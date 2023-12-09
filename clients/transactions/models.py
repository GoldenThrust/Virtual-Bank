from django.db import models
from accounts.models import Account
import uuid

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
        ('DEBIT_CARD', 'Debit Card'),
        ('PAYMENT', 'Payment'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=11)
    account_number = models.BigIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default="DEPOSIT")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction ID: {self.pk} - Type: {self.get_transaction_type_display()} - Amount: {self.amount}"
