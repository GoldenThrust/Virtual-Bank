from rest_framework import serializers
from .models import DebitCard
from credit_cards.serializers import generate_valid_credit_card_number, generate_cvv


class DebitCardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(read_only=True)
    cvv = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DebitCard
        fields = ["account", "card_number", "cvv", "expiration_date", "created_date"]

    def create(self, validated_data):
        validated_data["card_number"] = generate_valid_credit_card_number()
        validated_data["cvv"] = generate_cvv(
            validated_data["card_number"], validated_data["expiration_date"]
        )
        credit_card = DebitCard.objects.create(**validated_data)
        return credit_card
