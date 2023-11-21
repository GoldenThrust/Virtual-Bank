from rest_framework import serializers
from .models import Account
import random


def generate_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(12))


class AccountSerializer(serializers.ModelSerializer):
    number = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    extra_kwargs = {"currency": {"read_only": True}}

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "name",
            "account_type",
            "balance",
            "number",
            "currency",
            "created_date",
        ]

    def create(self, validated_data):
        validated_data["number"] = generate_account_number()
        account = Account.objects.create(**validated_data)
        return account


class AccountCreateSerializer(serializers.ModelSerializer):
    number = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    extra_kwargs = {
        "currency": {"read_only": True},
        "user": {"read_only": True},
    }

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "account_type",
            "balance",
            "number",
            "currency",
            "created_date",
        ]

    def create(self, validated_data):
        validated_data["number"] = generate_account_number()
        account = Account.objects.create(**validated_data)
        return account
