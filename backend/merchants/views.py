from django.shortcuts import render
from .serializers import MerchantSerializer, MerchantCreateSerializer
from rest_framework.exceptions import PermissionDenied
from .models import Merchant
from rest_framework import generics
from rest_framework import permissions

from accounts.models import Account


class MerchantList(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAdminUser]


class MerchantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAdminUser]


class MerchantCreate(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        accounts = Account.objects.filter(account__user=self.request.
        user)

        i = 0

        for account in accounts:
            i += 1
            if account.user == self.user:
                break
            if (i >= len(account)):
                raise PermissionDenied("Permission denied")

        serializer.save(user=self.request.user)

        


class MerchantDataManipulator(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        merchant = Merchant.objects.filter(user=user).first()
        if not merchant:
            raise PermissionDenied("Merchant account not found for this user")
        return merchant

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.delete()