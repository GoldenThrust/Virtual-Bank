from rest_framework import serializers
from .models import DebitCard, DebitCardTransaction
from .utils import generate_valid_credit_card_number, generate_cvv
from accounts.serializers import AccountSerializer
from transactions.serializers import TransactionSerializer


class DebitCardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(read_only=True)
    cvv = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    account = AccountSerializer()
    expiration_date = serializers.SerializerMethodField()

    class Meta:
        model = DebitCard
        fields = ["id", "account", "card_number", "cvv", "expiration_date", "created_date"]

    def create(self, validated_data):
        validated_data["card_number"] = generate_valid_credit_card_number()
        validated_data["cvv"] = generate_cvv(
            validated_data["card_number"], validated_data["expiration_date"]
        )
        credit_card = DebitCard.objects.create(**validated_data)
        return credit_card

    def get_expiration_date(self, obj):
        return obj.expiration_date.strftime("%m/%y") if obj.expiration_date else None


class TransactionDebitCardSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    transaction_partner_account = AccountSerializer()
    transaction_direction = serializers.SerializerMethodField()

    class Meta:
        model = DebitCardTransaction
        fields = "__all__"

    def get_transaction_direction(self, obj):
        request_user = self.context["request"].user
        if request_user == obj.transaction_partner_account.user or request_user != obj.transaction.account.user:
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