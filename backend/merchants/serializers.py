from rest_framework import serializers
from .models import Merchant
from accounts.serializers import AccountSerializer
import secrets
import string

def generate_api_key():
    """Generate a random API key."""
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for _ in range(32))
    return api_key

class MerchantSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True)
    api_key = serializers.CharField(read_only=True)
    account = AccountSerializer(read_only=True)
    account_number = serializers.CharField(write_only=True)


    class Meta:
        model = Merchant
        fields = ['account', 'account_number', 'description', 'category', 'payment_methods_accepted', 'business_hours', 'website_url', 'api_key', 'created_date']
        
        extra_kwargs = {
            "account": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data['api_key'] = generate_api_key()
        return super().create(validated_data)