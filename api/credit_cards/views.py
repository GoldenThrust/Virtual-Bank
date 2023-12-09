from django.shortcuts import render
from .serializers import CreditCardSerializer
from .models import CreditCard
from rest_framework import generics
from rest_framework import exceptions

from rest_framework import permissions


class CreditCardList(generics.ListCreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAdminUser]


class CreditCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAdminUser]


class UserCreditCardList(generics.ListAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CreditCard.objects.filter(account__user=user)

class UserCreditCardDetail(generics.RetrieveAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    lookup_field = 'number'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        credit_card = CreditCard.objects.filter(account__number=self.kwargs['number']).first()
        if not credit_card:
            raise exceptions.NotFound("Credit Card not found for this Account.")
        return credit_card