from django.shortcuts import render
from .serializers import CreditCardSerializer
from .models import CreditCard
from rest_framework import generics
# Create your views here.

class CreditCardList(generics.ListCreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class CreditCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer