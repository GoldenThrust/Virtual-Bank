from django.shortcuts import render
from .serializers import AccountSerializer, AccountCreateSerializer
from .models import Account
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from debit_cards.models import DebitCard
from credit_cards.serializers import generate_cvv, generate_valid_credit_card_number
import datetime
from notifications.utils import process_notifications

from rest_framework import permissions


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
        account_name = self.request.data.get("account_type")
        account_type = self.request.data.get("account_type")

        existing_account = Account.objects.filter(user=self.request.user, name=account_name).exists()
        if existing_account:
            raise exceptions.PermissionDenied('Account with this name already exists for the user')

        account = serializer.save(user=self.request.user)

        # notification
        notification_message  = 'A new Account has been successfully created.'
        process_notifications(self.request.user, 'account_notification', notification_message)

        if account_type == "CURRENT":
            debit_card = DebitCard(account=account)
            card_number = generate_valid_credit_card_number()
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=365 * 3)
            debit_card.card_number = card_number
            debit_card.cvv = generate_cvv(card_number, expiry_date)
            debit_card.expiration_date = expiry_date
            debit_card.save()

             # notification
            notification_message = f'A debit card has been successfully created for your account ({account.number}).'
            process_notifications(self.request.user, 'account_notification', notification_message)


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
            raise exceptions.NotFound("Not found")

        return account

    def perform_update(self, serializer):
        serializer.validated_data.pop('account_type', None)
        serializer.validated_data.pop('balance', None)
        serializer.validated_data.pop('currency', None)
        account_name = serializer.validated_data.get('name')
        existing_account = Account.objects.filter(user=self.request.user, name=account_name).exists()
        if existing_account:
            raise exceptions.PermissionDenied('Account with this name already exists for the user')

        serializer.save(user=self.request.user)

        # notification
        notification_message = 'Account updated successfully'
        process_notifications(self.request.user, 'account_notification', notification_message)

    def perform_destroy(self, instance):
        instance.delete()

        # notification
        notification_message  = 'Account deleted successfully'
        process_notifications(self.request.user, 'account_notification', notification_message)