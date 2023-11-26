from django.shortcuts import render
from .serializers import TransferSerializer
from .models import Transfer
from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions, exceptions


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
        debit_card = Transfer.objects.filter(
            transaction__identifier=self.kwargs["identifier"]
        ).first()

        if not debit_card:
            raise exceptions.NotFound()

        return debit_card