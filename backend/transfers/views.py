from django.shortcuts import render
from .serializers import TransferSerializer
from .models import Transfer
from rest_framework import generics

from rest_framework import permissions

class TransferList(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAdminUser]


class TransferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAdminUser]
