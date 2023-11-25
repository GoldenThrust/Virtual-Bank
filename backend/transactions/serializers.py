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
    transaction_partner_account_number = serializers.CharField(write_only=True)
    account = AccountSerializer(read_only=True)
    account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "account",
            "account_number",
            "transaction_partner_account_number",
            "transaction_type",
            "amount",
            "identifier",
            "date",
        ]

        extra_kwargs = {
            "transaction_type": {"read_only": True},
        }


class DebitCardPaymentSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    cvv = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True)
    expiry_date = serializers.CharField(write_only=True)
    cvv = serializers.CharField(write_only=True)


    class Meta:
        model = Transaction
        fields = [
            "account",
            "account_number",
            "card_number",
            "transaction_type",
            "expiry_date",
            "cvv",
            "amount",
            "identifier",
            "date",
        ]
