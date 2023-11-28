from django.shortcuts import render
from .serializers import MerchantSerializer
from rest_framework import exceptions
from .models import Merchant
from rest_framework import generics
from rest_framework import permissions
from notifications.utils import process_notifications
from accounts.models import Account


class MerchantList(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAdminUser]


class MerchantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAdminUser]


class MerchantCreate(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user_name = f'{user.first_name} {user.last_name}'
        account = Account.objects.get(
            number=serializer.validated_data.pop("account_number")
        )

        if not account:
            raise exceptions.NotFound()

        if account.user != user:
            notification_message = f'An attempt was made by {user_name} to create a merchant account using your account number ({account.number}).'
            process_notifications(user, 'security_notification', notification_message)
            raise exceptions.NotFound()

        merchant = Merchant.objects.filter(account=account)
        if merchant:
            raise exceptions.PermissionDenied("Merchant Account Exists")

        serializer.save(account=account)
        notification_message = f'Merchant account has been successfully created. The account number ({account.number}) is now linked to a merchant account.'
        process_notifications(user, 'user_notification', notification_message)




class MerchantDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        merchant = Merchant.objects.filter(account__user=user).first()
        if not merchant:
            raise exceptions.NotFound()
        return merchant

    def perform_update(self, serializer):
        if serializer.validated_data['account_number']:
            serializer.validated_data.pop('account_number')
        serializer.save(account__user=self.request.user)
        notification_message  = 'Merchant Account updated successfully'
        process_notifications(self.request.user, 'user_notification', notification_message)

    def perform_destroy(self, instance):
        instance.delete()
        notification_message  = 'Merchant Account deleted successfully'
        process_notifications(self.request.user, 'user_notification', notification_message)
