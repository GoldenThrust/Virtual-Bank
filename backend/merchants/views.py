from django.shortcuts import render
from .serializers import MerchantSerializer
from .models import Merchant
from rest_framework import generics
# Create your views here.

class MerchantList(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer


class MerchantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer