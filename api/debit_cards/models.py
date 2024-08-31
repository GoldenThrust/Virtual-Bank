from django.db import models
from accounts.models import Account
from transactions.models import Transaction
from transactions.utils import convert_currency


class DebitCard(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.BigIntegerField()
    cvv = models.CharField(max_length=4)
    expiration_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - User: {self.account.user.first_name} {self.account.user.last_name}"