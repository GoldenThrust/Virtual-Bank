from django.db import models
from accounts.models import Account
from transactions.models import Transaction

class Transfer(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='transfer')
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_transfers')

    def __str__(self):
        return f"Transfer ID: {self.pk} - Sender: {self.sender_account.user.username} - Receiver: {self.receiver_account.user.username} - Amount: {self.amount}"
