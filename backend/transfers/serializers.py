from rest_framework import serializers
from .models import Transfer
from transactions.serializers import TransactionSerializer

class TransferSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()

    class Meta:
        model = Transfer
        fields = ['transaction', 'receiver_account']