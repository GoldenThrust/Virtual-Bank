from django.shortcuts import render
from .serializers import TransferSerializer
from .models import Transfer
from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions, exceptions
from notifications.utils import process_notifications
from django.utils.timezone import localtime

class TransferList(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAdminUser]


class TransferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAdminUser]


class UserTransferList(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transfer.objects.filter(
            Q(transaction__account__user=user)
            | Q(transaction_partner_account__user=user)
        )

class UserTransferDetails(generics.RetrieveAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        transfer = Transfer.objects.filter(
            transaction__identifier=self.kwargs["identifier"]
        ).first()

        if not transfer:
            raise exceptions.NotFound()
        
        transfer_user = transfer.transaction.account.user
        transaction_partner = transfer.transaction_partner_account.user
        if self.request.user != transfer_user and self.request.user != transaction_partner:
            peek_user = self.request.user
            transaction_date = localtime(transfer.transaction.date).strftime('%m/%d/%Y at %I:%M %p')
            user_name = f'{peek_user.first_name} {peek_user.last_name}'
            if peek_user.is_superuser:
                user_name = 'Virtual-Bank administrator'
            
            # notification
            notification_message = f'{user_name} reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(transfer_user, 'security_notification', notification_message)
            process_notifications(transaction_partner, 'security_notification', notification_message)

        return transfer