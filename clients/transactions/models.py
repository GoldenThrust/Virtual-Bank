from django.db import models
from accounts.models import Account
import uuid

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
        ('DEBIT_CARD', 'Debit Card'),
        ('PAYMENT', 'Payment'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=11)
    account_number = models.BigIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default="DEPOSIT")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    # @classmethod
    # def get_top_10_partners(cls, account_id):
    #     top_partners = cls.objects.filter(account=account_id).filter(
    #         models.Q(debit_card__isnull=False) | models.Q(transfer__isnull=False)
    #     )

    #     partner_account_numbers = top_partners.values_list(
    #         *('debit_card__transaction_partner_account',
    #         'transfer__transaction_partner_account')
    #     ).distinct().order_by('-amount')[:10]

    #     return partner_account_numbers

    def __str__(self):
        return f"Transaction ID: {self.pk} - Type: {self.get_transaction_type_display()} - Amount: {self.amount}"
