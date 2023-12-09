from django.db import models
from accounts.models import Account
from transactions.models import Transaction

class Transfer(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='transfer')
    transaction_partner_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transaction_partner_transfers')

    def __str__(self):
        return f"Transfer ID: {self.pk} - Sender: {self.transaction.account.user.first_name} {self.transaction.account.user.last_name} - Transaction partner: {self.transaction_partner_account.user.first_name} {self.transaction_partner_account.user.last_name} - Amount: {self.transaction.amount}"
