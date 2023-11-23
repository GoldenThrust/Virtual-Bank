from django.shortcuts import render
from .serializers import DebitCardSerializer
from .models import DebitCard
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from rest_framework import permissions


class DebitCardList(generics.ListCreateAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class DebitCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardSerializer
    permission_classes = [permissions.IsAdminUser]


class DebitCardList(generics.ListAPIView):
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
    lookup_field = 'pk'

    def get_object(self):
        user = self.request.user
        credit_card = DebitCard.objects.filter(pk=self.kwargs['pk'], account__user=user).first()
        if not credit_card:
            raise PermissionDenied("Debit Card not found for this Account.")
        return credit_card