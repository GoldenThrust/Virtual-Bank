from django.shortcuts import render
from .serializers import DebitCardSerializer
from .models import DebitCard
from accounts.models import Account
from rest_framework import generics
from rest_framework import exceptions

from rest_framework import permissions


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
    lookup_field = "number"

    def get_object(self):
        user = self.request.user
        print(self.kwargs)
        debit_card = DebitCard.objects.filter(
            account__number=self.kwargs["number"]
        ).first()
        if not debit_card:
            raise exceptions.NotFound()
        return debit_card
