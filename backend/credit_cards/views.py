from django.shortcuts import render
from .serializers import CreditCardSerializer
from .models import CreditCard
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from rest_framework import permissions


class CreditCardList(generics.ListCreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAdminUser]


class CreditCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAdminUser]


class CreditCardList(generics.ListAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CreditCard.objects.filter(account__user=user)

# class UserCreditCardDetail(generics.RetrieveUpdateAPIView):
class UserCreditCardDetail(generics.RetrieveAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        credit_card = CreditCard.objects.filter(pk=self.kwargs['pk'], account__user=user).first()
        if not credit_card:
            raise PermissionDenied("Credit Card not found for this Account.")
        return credit_card