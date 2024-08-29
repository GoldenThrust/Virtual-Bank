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
    
class DebitCardTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='debit_card')
    transaction_partner_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transaction_partner_debit_card')
    
    def get_transfer_currency_conversion(self):
        source_currency = self.transaction_partner_account.currency
        target_currency = self.transaction.account.currency
        converted_amount = convert_currency(self.transaction.amount, source_currency, target_currency)
        return converted_amount

    def __str__(self):
        return f"Transfer ID: {self.pk} - Receiver: {self.transaction.account.user.first_name} {self.transaction.account.user.last_name} - Transaction_partner: {self.transaction_partner_account.user.first_name} {self.transaction_partner_account.user.last_name} - Amount: {self.transaction.amount}"