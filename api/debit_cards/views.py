from django.shortcuts import render
from .serializers import DebitCardSerializer
from .models import DebitCard
from accounts.models import Account
from rest_framework import generics
from rest_framework import exceptions
from django.db.models import Q
from rest_framework import permissions
from notifications.utils import process_notifications
from django.utils.timezone import localtime


class DebitCardList(generics.ListCreateAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class DebitCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
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

    def get_object(self):
        user = self.request.user
        number = self.kwargs["number"]

        debit_card = DebitCard.objects.filter(card_number=number, account__user=user).first()


        if not debit_card:
            raise exceptions.NotFound()

        return debit_card


# def renewDebitCard():
#     pass
