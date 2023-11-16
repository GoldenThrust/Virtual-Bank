from django.db import models
from accounts.models import Account

class Transfer(models.Model):
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_transfers')
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_transfers')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    token = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Transfer ID: {self.pk} - Sender: {self.sender_account.user.username} - Receiver: {self.receiver_account.user.username} - Amount: {self.amount}"
