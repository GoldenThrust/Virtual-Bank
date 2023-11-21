from django.db import models
from accounts.models import Account
import datetime


class CreditCard(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    available_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=2000.00
    )

    card_number = models.BigIntegerField()
    cvv = models.CharField(max_length=4)
    expiration_date = models.DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(days=365 * 3)
    )

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - User: {self.account.user.username}"
