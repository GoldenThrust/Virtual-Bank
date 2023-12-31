from rest_framework import serializers
from .models import Transaction
from accounts.serializers import AccountSerializer


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    account = AccountSerializer(read_only=True)
    account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
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


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["transaction_type"]

    # Custom representation method to handle serialization based on transaction type
    def to_representation(self, instance):
        from transfers.serializers import TransferSerializer
        from debit_cards.serializers import TransactionDebitCardSerializer
        from deposits.serializers import DepositSerializer

        # Fetching transaction type, current user, and URL name from context
        transaction_type = instance.transaction_type
        user = self.context['request'].user
        url_name = self.context['request'].resolver_match.url_name
        
        # Initializing serializer and related_instance variables
        serializer = None
        related_instance = None
        
        # Checking transaction type and assigning related instance accordingly
        if transaction_type == 'TRANSFER':
            related_instance = instance.transfer
        elif transaction_type == 'DEBIT_CARD':
            related_instance = instance.debit_card
        elif transaction_type == 'DEPOSIT':
            related_instance = instance.deposit
        
        if related_instance:
            # Checking permissions based on transaction type and user access
            if transaction_type == 'DEPOSIT' or (related_instance.transaction.account.user == user or url_name == 'transactions_detail'):
                # Initializing the appropriate serializer based on transaction type
                if transaction_type == 'TRANSFER':
                    serializer = TransferSerializer(instance=related_instance, context={'request': self.context['request']})
                elif transaction_type == 'DEBIT_CARD':
                    serializer = TransactionDebitCardSerializer(instance=related_instance, context={'request': self.context['request']})
                elif transaction_type == 'DEPOSIT':
                    serializer = DepositSerializer(instance=related_instance, context={'request': self.context['request']})

        # Returning serialized data if serializer exists and has a 'data' attribute, otherwise None
        return serializer.data if (serializer and hasattr(serializer, 'data')) else serializer



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
