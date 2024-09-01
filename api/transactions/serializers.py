from rest_framework import serializers
from .models import Transaction
from accounts.serializers import AccountSerializer

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    payer = AccountSerializer()
    payee = AccountSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    account = AccountSerializer(read_only=True)
    amount_received = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    account_number = serializers.CharField(write_only=True)
    amount = serializers.IntegerField(write_only=True)
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES, read_only=True, default="DEPOSIT")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "amount",
            "amount_received",
            "account_number",
            "transaction_type",
            "identifier",
            "date",
        ]

        extra_kwargs = {
            "transaction_type": {"read_only": True, "default": "DEPOSIT"},
            "account": {"read_only": True},
        }
  

class TransferSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    account = AccountSerializer(read_only=True)
    payer = AccountSerializer(read_only=True)
    payee = AccountSerializer(read_only=True)
    payer_account_number = serializers.CharField(write_only=True)
    payee_account_number = serializers.CharField(write_only=True)
    amount = serializers.IntegerField(write_only=True)
    amount_sent = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    amount_received = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    currency_sent = serializers.CharField(read_only=True)
    currency_received = serializers.CharField(read_only=True)
    rate = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True)
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES, read_only=True, default="TRANSFER")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "payer",
            "payee",
            "amount",
            "amount_sent",
            "amount_received",
            "currency_sent",
            "currency_received",
            "rate",
            "payer_account_number",
            "payee_account_number",
            "transaction_type",
            "identifier",
            "date",
        ]
        
        


class DebitCardTransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    account = AccountSerializer(read_only=True)
    payer = AccountSerializer(read_only=True)
    payee = AccountSerializer(read_only=True)
    amount = serializers.IntegerField(write_only=True)
    amount_sent = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    payee_account_number = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True)
    cvv = serializers.CharField(max_length=4, write_only=True)
    expiration_date = serializers.CharField(write_only=True)
    amount_received = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    currency_sent = serializers.CharField(read_only=True)
    currency_received = serializers.CharField(read_only=True)
    rate = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True)
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES, read_only=True, default="DEBIT_CARD")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "payer",
            "payee",
            "amount",
            "amount_sent",
            "amount_received",
            "currency_sent",
            "currency_received",
            "payee_account_number",
            "card_number",
            "cvv",
            "expiration_date",  
            "rate",
            "transaction_type",
            "identifier",
            "date",
        ]
      