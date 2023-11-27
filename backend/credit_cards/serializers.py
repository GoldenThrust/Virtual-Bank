from rest_framework import serializers
from .models import CreditCard
from debit_cards.utils import generate_valid_credit_card_number, generate_cvv

class CreditCardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(read_only=True)
    cvv = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CreditCard
        fields = ['account', 'limit', 'available_credit', 'card_number', 'cvv', 'expiration_date', 'created_date']

    def create(self, validated_data):
        validated_data['card_number'] = generate_valid_credit_card_number()
        validated_data['cvv'] = generate_cvv(validated_data['card_number'], validated_data['expiration_date'])
        credit_card = CreditCard.objects.create(**validated_data)
        return credit_card