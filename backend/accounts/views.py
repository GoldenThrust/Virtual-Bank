from django.shortcuts import render
from .serializers import AccountSerializer, AccountCreateSerializer
from .models import Account
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from credit_cards.models import CreditCard
from credit_cards.serializers import generate_cvv, generate_valid_credit_card_number
import datetime


from rest_framework import permissions
from users.permissions import IsOwnerOrReadOnly


class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]


class AccountCreate(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account_type = self.request.data.get("account_type")

        account = serializer.save(user=self.request.user)
        if account_type == "CREDIT_CARD":
            credits = CreditCard(account=account)
            card_number = generate_valid_credit_card_number()
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=365 * 3)
            credits.card_number = card_number
            credits.cvv = generate_cvv(card_number, expiry_date)
            print(credits)
            credits.expiration_date = expiry_date
            credits.save()


class UserAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        account = Account.objects.filter(user=user).first()
        if not account:
            raise PermissionDenied("Account not found for this user")
        return account

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
