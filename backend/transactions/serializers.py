from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'identifier', 'date']