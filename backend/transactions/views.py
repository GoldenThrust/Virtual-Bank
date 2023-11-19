from django.shortcuts import render
from .serializers import TransactionSerializer
from .models import Transaction
from rest_framework import generics
# Create your views here.

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer