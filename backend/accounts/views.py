from django.shortcuts import render
from .serializers import AccountSerializer, AccountCreateSerializer
from .models import Account
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from debit_cards.models import DebitCard
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
        duplicate_account = Account.objects.filter(name=serializer.validated_data['name'])

        if duplicate_account:
            raise PermissionDenied("account with this name already exists.")

        account = serializer.save(user=self.request.user)
        if account_type == "CURRENT":
            debit_card = DebitCard(account=account)
            card_number = generate_valid_credit_card_number()
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=365 * 3)
            debit_card.card_number = card_number
            debit_card.cvv = generate_cvv(card_number, expiry_date)
            debit_card.expiration_date = expiry_date
            debit_card.save()


class UserAccountList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)


class UserAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'number'

    def get_object(self):
        user = self.request.user
        account = Account.objects.filter(user=user, number=self.kwargs['number']).first()
        if not account:
            raise PermissionDenied("Not found")

        return account

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
