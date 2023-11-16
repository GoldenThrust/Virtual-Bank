from django.db import models
from accounts.models import Account
import uuid

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
        ('PAYMENT', 'Payment'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Transaction ID: {self.pk} - Type: {self.get_type_display()} - Amount: {self.amount}"
