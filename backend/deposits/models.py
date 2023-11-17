from django.db import models
from accounts.models import Account
from transactions.models import Transaction

class Deposit(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='deposit')

    def __str__(self):
        return f"Deposit ID: {self.deposit_id} - Account: {self.account.number} - Amount: {self.amount}"
