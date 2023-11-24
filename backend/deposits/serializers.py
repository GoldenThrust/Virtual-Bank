from rest_framework import serializers
from .models import Deposit
from transactions.serializers import TransactionSerializer


class DepositSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()

    class Meta:
        model = Deposit
        fields = ['transaction']