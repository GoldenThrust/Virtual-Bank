from django.shortcuts import render
from .serializers import AccountSerializer
from .models import Account
from rest_framework import generics
# Create your views here.

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer