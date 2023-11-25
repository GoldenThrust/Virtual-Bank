import json
from rest_framework import serializers
from .models import Transfer
from transactions.serializers import TransactionSerializer

class TransferSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    transaction_partner_account = serializers.SerializerMethodField()

    class Meta:
        model = Transfer
        fields = ['transaction', 'transaction_partner_account']

    def get_transaction_partner_account(self, obj):
        transaction_partner_account = None
        if obj.transaction_partner_account:
            transaction_partner_account = obj.transaction_partner_account
            transaction_partner_info = {'name': f'{transaction_partner_account.user.first_name} {transaction_partner_account.user.last_name}', 'number': transaction_partner_account.number}

        return (transaction_partner_info)