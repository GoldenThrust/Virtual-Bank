from django.shortcuts import render
from .serializers import DepositSerializer
from .models import Deposit
from transactions.models import Transaction
from rest_framework import generics, permissions, exceptions
from notifications.utils import process_notifications
from django.utils.timezone import localtime

class DepositList(generics.ListCreateAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAdminUser]


class DepositDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDepositList(generics.ListAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Deposit.objects.filter(transaction__account__user=user)
    


class UserDepositDetail(generics.RetrieveAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "identifier"

    def get_object(self):
        deposit = Deposit.objects.filter(
            transaction__identifier=self.kwargs["identifier"]
        ).first()

        if not deposit:
            raise exceptions.NotFound()

        if self.request.user != deposit.transaction.account.user:
            peek_user = self.request.user
            transaction_date = localtime(deposit.transaction.date).strftime('%m/%d/%Y')
            user_name = f'{peek_user.first_name} {peek_user.last_name}'
            notification_message = f'{user_name} has reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(deposit.transaction.account.user, 'security_notification', notification_message)
        return deposit