from django.shortcuts import render
from .serializers import DepositSerializer
from .models import Deposit
from transactions.models import Transaction
from rest_framework import generics, permissions, exceptions


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
        debit_card = Deposit.objects.filter(
            transaction__identifier=self.kwargs["identifier"]
        ).first()

        if not debit_card:
            raise exceptions.NotFound()

        return debit_card