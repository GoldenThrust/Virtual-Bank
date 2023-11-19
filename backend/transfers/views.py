from django.shortcuts import render
from .serializers import TransferSerializer
from .models import Transfer
from rest_framework import generics
# Create your views here.

class TransferList(generics.ListCreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class TransferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer