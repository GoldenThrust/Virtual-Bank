from rest_framework import serializers
from .models import Account
from .utils import generate_account_number


class AccountSerializer(serializers.ModelSerializer):
    number = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Account
        number = serializers.IntegerField(read_only=True)

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

        extra_kwargs = {
            "user": {"read_only": True},
        }

    def get_user(self, obj):
        return (f"{obj.user.first_name} {obj.user.last_name}") if obj.user else None

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
            "id",
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
