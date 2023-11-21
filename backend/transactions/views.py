from django.shortcuts import render
from .serializers import TransactionSerializer
from .models import Transaction
from transfers.models import Transfer
from accounts.models import Account
from rest_framework import generics
import json
# Create your views here.

class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# def Transfer(account, receiver_account_number, amount):
#     reciever_account= Account.objects.filter(number=receiver_account_number)

#     transaction = Transaction.objects.create(account=account, amount=amount, transaction_type="TRANSFER")
#     transfer = Transfer.objects.create(transaction=transaction, sender_account=account, receiver_account=reciever_account)

#     sender = Account.objects.filter(user=account.user)
#     reciever = Account.objects.filter(user=reciever_account.user)

#     if (sender.balance > amount):
#         sender.balance - amount
#         reciever.balance += amount

#         sender.save()
#         reciever.save()
#     else:
#         try:
#             raise InsufficentBalanceException("Insufficient funds")
#         except Exception:
#             return json.loads({"error": Exception })
