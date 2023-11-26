import json
from rest_framework import serializers
from .models import Transfer
from transactions.serializers import TransactionSerializer
from accounts.serializers import AccountSerializer

class TransferSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    transaction_partner_account = AccountSerializer()
    transaction_direction = serializers.SerializerMethodField()

    class Meta:
        model = Transfer
        fields = ['transaction', 'transaction_partner_account', 'transaction_direction']
    
    
    def get_transaction_direction(self, obj):
        request_user = self.context["request"].user
        if request_user == obj.transaction.account.user:
            return "DEBITED"
        else:
            return "CREDITED"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request_user = self.context["request"].user

        if request_user == instance.transaction_partner_account.user:
            ret["transaction_partner_account"], ret["transaction"]["account"] = (
                ret["transaction"]["account"],
                ret["transaction_partner_account"],
            )
        
        ret["transaction_partner_account"].pop("balance", None)

        if not (request_user == instance.transaction_partner_account.user or request_user == instance.transaction.account.user):
            ret["transaction"]['account'].pop("balance", None)

        return ret
