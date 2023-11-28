from django.shortcuts import render
from .serializers import DebitCardSerializer, TransactionDebitCardSerializer
from .models import DebitCard, DebitCardTransaction
from accounts.models import Account
from rest_framework import generics
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import permissions


class DebitCardList(generics.ListCreateAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class DebitCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class TransactionDebitCard(generics.ListCreateAPIView):
    queryset = DebitCardTransaction.objects.all()
    serializer_class = TransactionDebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class TransactionDebitCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DebitCardTransaction.objects.all()
    serializer_class = TransactionDebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDebitCardList(generics.ListAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DebitCard.objects.filter(account__user=user)


class UserDebitCardDetail(generics.RetrieveAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "number"

    def get_object(self):
        user = self.request.user
        debit_card = DebitCard.objects.filter(
            account__number=self.kwargs["number"]
        ).first()

        if not debit_card:
            raise exceptions.NotFound()

        return debit_card


class UserTransactionDebitCardList(generics.ListAPIView):
    queryset = DebitCardTransaction.objects.all()
    serializer_class = TransactionDebitCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DebitCardTransaction.objects.filter(
            Q(transaction__account__user=user) | Q(transaction_partner_account__user=user)
        )


class UserTransactionDebitCardDetail(generics.RetrieveAPIView):
    queryset = DebitCardTransaction.objects.all()
    serializer_class = TransactionDebitCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "identifier"

    def get_object(self):
        debit_card = DebitCardTransaction.objects.filter(
            transaction__identifier=self.kwargs["identifier"]
        ).first()

        if not debit_card:
            raise exceptions.NotFound()
        
        # if self.request.user != debit_card.account.user:
        #     peek_user = self.request.user
        #     transaction_date = localtime(debit_card.transaction.date).strftime('%m/%d/%Y')
        #     user_name = f'{peek_user.first_name} {peek_user.last_name}'
        #     notification_message = f'{user_name} has reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
        #     process_notifications(debit_card.account.user, 'security_notification', notification_message)

        return debit_card