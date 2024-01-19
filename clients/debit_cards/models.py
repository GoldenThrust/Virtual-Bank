from django.db import models
from accounts.models import Account
import datetime
from transactions.models import Transaction


class DebitCard(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.BigIntegerField()
    cvv = models.CharField(max_length=4)
    expiration_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - User: {self.account.user.first_name} {self.account.user.last_name}"
    
class DebitCardTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='debit_card')
    transaction_partner_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transaction_partner_debit_card')

    def __str__(self):
        return f"Debit Card Transansaction ID: {self.pk} - Receiver: {self.transaction.account.user.first_name} {self.transaction.account.user.last_name} - Transaction_partner: {self.transaction_partner_account.user.first_name} {self.transaction_partner_account.user.last_name} - Amount: {self.transaction.amount}"