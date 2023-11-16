from django.db import models
from encrypted_model_fields.fields import EncryptedCharField, EncryptedDateField
from accounts.models import Account

class CreditCard(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    available_credit = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)

    card_number = EncryptedCharField(max_length=16)
    cvv = EncryptedCharField(max_length=4)
    expiration_date = EncryptedDateField()

    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - User: {self.account.user.username}"