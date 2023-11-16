from django.db import models
from accounts.models import Account

class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Deposit ID: {self.deposit_id} - Account: {self.account.number} - Amount: {self.amount}"
