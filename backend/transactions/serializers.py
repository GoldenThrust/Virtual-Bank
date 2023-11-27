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

    def to_representation(self, instance):
        from transfers.serializers import TransferSerializer
        from debit_cards.serializers import TransactionDebitCardSerializer
        from deposits.serializers import DepositSerializer
        transaction_type = instance.transaction_type

        serializer = None
        user = self.context['request'].user
        url_name = self.context['request'].resolver_match.url_name
    
        if transaction_type == 'TRANSFER':
            transfer_instance = instance.transfer
            if (transfer_instance.transaction.account.user == user or transfer_instance.transaction_partner_account.user == user) or url_name == 'transactions_detail':
                serializer = TransferSerializer(instance=transfer_instance, context={'request': self.context['request']})
        elif transaction_type == 'DEBIT_CARD':
            debit_card_instance = instance.debit_card
            if (debit_card_instance.transaction.account.user == user or debit_card_instance.transaction_partner_account.user == user) or url_name == 'transactions_detail':
                serializer = TransactionDebitCardSerializer(instance=debit_card_instance, context={'request': self.context['request']})
        elif transaction_type == 'DEPOSIT':
            deposit_instance = instance.deposit
            if deposit_instance.transaction.account.user == user or url_name == 'transactions_detail':
                serializer = DepositSerializer(instance=deposit_instance, context={'request': self.context['request']})
        if serializer:
            if hasattr(serializer, 'data'):
                return serializer.data
            else:
                return serializer
        else:
            return None



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
