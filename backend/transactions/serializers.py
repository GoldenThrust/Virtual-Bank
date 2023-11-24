from rest_framework import serializers
from .models import Transaction
from accounts.serializers import AccountSerializer


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    account = AccountSerializer()
    account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "account",
            "account_number",
            "transaction_type",
            "amount",
            "identifier",
            "date",
        ]

        extra_kwargs = {
            "account": {"read_only": True},
        }


class TransferTransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    receiver_account_number = serializers.CharField(write_only=True)
    account = AccountSerializer()
    account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "account",
            "receiver_account_number",
            "transaction_type",
            "amount",
            "identifier",
            "date",
        ]

        extra_kwargs = {
            "account": {"read_only": True},
        }
