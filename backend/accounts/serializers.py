from rest_framework import serializers
from .models import Account
from users.serializers import UserSerializer
import random


def generate_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(12))


class AccountSerializer(serializers.ModelSerializer):
    number = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "user",
            "name",
            "account_type",
            "balance",
            "number",
            "currency",
            "created_date",
        ]

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def create(self, validated_data):
        validated_data["number"] = generate_account_number()
        account = Account.objects.create(**validated_data)
        return account


class AccountCreateSerializer(serializers.ModelSerializer):
    number = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    user = serializers.SerializerMethodField()


    class Meta:
        model = Account
        fields = [
            "user",
            "name",
            "account_type",
            "balance",
            "number",
            "currency",
            "created_date",
        ]

        extra_kwargs = {
        "user": {"read_only": True},
        }

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def create(self, validated_data):
        validated_data["number"] = generate_account_number()
        account = Account.objects.create(**validated_data)
        return account
