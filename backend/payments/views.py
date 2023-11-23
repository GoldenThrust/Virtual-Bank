from django.shortcuts import render
from .serializers import PaymentSerializer
from .models import Payment
from rest_framework import generics

from rest_framework import permissions


class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]
