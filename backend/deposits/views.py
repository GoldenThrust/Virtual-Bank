from django.shortcuts import render
from .serializers import DepositSerializer
from .models import Deposit
from rest_framework import generics
# Create your views here.

class DepositList(generics.ListCreateAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer


class DepositDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer