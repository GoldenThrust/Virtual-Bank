from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account_number",
            "transaction_type",
            "amount",
            "identifier",
            "date",
        ]


class TransferTransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    receiver_account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account_number",
            "receiver_account_number",
            "transaction_type",
            "amount",
            "identifier",
            "date",
        ]
