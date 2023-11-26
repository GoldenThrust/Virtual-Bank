from rest_framework import serializers
from .models import Deposit
from transactions.serializers import TransactionSerializer


class DepositSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()

    class Meta:
        model = Deposit
        fields = ['id', 'transaction']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request_user = self.context["request"].user

        if request_user != instance.transaction.account.user:
            ret["transaction"]['account'].pop("balance", None)

        return ret
