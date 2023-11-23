from django.shortcuts import render
from rest_framework import generics
import json

# Models and Serializers
from .models import Transaction
from accounts.models import Account
from deposits.models import Deposit
from payments.models import Payment
from transfers.models import Transfer
from .serializers import TransactionSerializer, TransferTransactionSerializer
# from deposits.serializers import DepositSerializer
# from payments.serializers import PaymentSerializer
# from transfers.serializers import TransferSerializer

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]


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


class TransactionDepositCreate(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account_number = serializer.validated_data.get("account_number")
        account = Account.objects.filter(number=account_number).first()

        if not account:
            raise PermissionDenied("Account not found")

        if account.user != self.request.user:
            raise PermissionDenied("Account does not belong to this user")

        serializer.save(transaction_type="DEPOSIT")

        # Update Account Balance
        transaction_amount = serializer.validated_data.get("amount")
        account.balance += transaction_amount
        account.save()

        # Create Deposit
        deposit = Deposit.objects.create(transaction=serializer.instance)


class MasterTransactionDetails(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransferTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    debit_account_number = None


class TransactionTransferCreate(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransferTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    receiver_account_number = None

    def perform_create(self, serializer):
        account_number = serializer.validated_data.get("account_number")
        account = Account.objects.filter(number=account_number).first()

        if not account:
            raise PermissionDenied("Account not found")

        if account.user != self.request.user:
            raise PermissionDenied("Account does not belong to this user")

        transaction_amount = serializer.validated_data.get("amount")
        self.receiver_account_number = serializer.validated_data.pop("receiver_account_number")

        if int(account_number) == int(self.receiver_account_number):
            raise PermissionDenied("Sender and receiver accounts cannot be the same")

        receiver_account = Account.objects.filter(
            number=self.receiver_account_number
        ).first()

        if not receiver_account:
            raise PermissionDenied("Receiver Account not found")
        

        if account.balance >= transaction_amount:
            serializer.save(transaction_type="TRANSFER")

            # Update Account Balances
            account.balance -= transaction_amount
            receiver_account.balance += transaction_amount

            account.save()
            receiver_account.save()

            # Create Transfer
            transfer = Transfer.objects.create(
                transaction=serializer.instance, receiver_account=receiver_account
            )
        else:
            raise PermissionDenied("Insufficient funds")
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serialized_data = serializer.data
        serialized_data['receiver_account_number'] = int(self.receiver_account_number)
        headers = self.get_success_headers(serializer.data)
        return Response(serialized_data, status=status.HTTP_201_CREATED, headers=headers)


class TransactionDebitCardCreate():
    queryset = Transaction.objects.all()
    serializer_class = TransferTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    debit_account_number = None