from django.shortcuts import render
from .serializers import PaymentSerializer
from .models import Payment
from rest_framework import generics
# Create your views here.

class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer