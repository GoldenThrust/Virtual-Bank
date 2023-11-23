from django.shortcuts import render
from .serializers import DepositSerializer
from .models import Deposit
from rest_framework import generics

from rest_framework import permissions

class DepositList(generics.ListCreateAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAdminUser]


class DepositDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAdminUser]
