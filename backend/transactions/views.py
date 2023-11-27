from django.shortcuts import render
from rest_framework import generics
import json
from datetime import datetime

# Models and Serializers
from .models import Transaction
from accounts.models import Account
from deposits.models import Deposit
from django.db.models import Q

# from payments.models import Payment
from transfers.models import Transfer
from .serializers import (
    TransactionSerializer,
    TransferTransactionSerializer,
    DebitCardPaymentSerializer,
    TransactionHistorySerializer,
)

# from deposits.serializers import DepositSerializer
# from payments.serializers import PaymentSerializer
# from transfers.serializers import TransferSerializer
from debit_cards.models import DebitCardTransaction, DebitCard

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import exceptions


class DateError(Exception):
    pass


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]


class TransactionDepositCreate(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account_number = serializer.validated_data.get("account_number")
        account = Account.objects.filter(number=account_number).first()

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != self.request.user:
            raise exceptions.PermissionDenied("Account does not belong to this user")

        serializer.save(transaction_type="DEPOSIT", account=account)

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
    transaction_partner_account_number = None

    def perform_create(self, serializer):
        account_number = serializer.validated_data.get("account_number")
        account = Account.objects.filter(number=account_number).first()

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != self.request.user:
            raise exceptions.PermissionDenied("Account does not belong to this user")

        transaction_amount = serializer.validated_data.get("amount")
        self.transaction_partner_account_number = serializer.validated_data.pop(
            "transaction_partner_account_number"
        )

        if int(account_number) == int(self.transaction_partner_account_number):
            raise exceptions.PermissionDenied(
                "Sender and transaction_partner accounts cannot be the same"
            )

        transaction_partner_account = Account.objects.filter(
            number=self.transaction_partner_account_number
        ).first()

        if not transaction_partner_account:
            raise exceptions.NotFound("Transaction_partner Account not found")

        if account.balance >= transaction_amount:
            serializer.save(transaction_type="TRANSFER", account=account)

            # Update Account Balances
            account.balance -= transaction_amount
            transaction_partner_account.balance += transaction_amount

            account.save()
            transaction_partner_account.save()

            # Create Transfer
            transfer = Transfer.objects.create(
                transaction=serializer.instance,
                transaction_partner_account=transaction_partner_account,
            )
        else:
            raise exceptions.PermissionDenied("Insufficient funds")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serialized_data = serializer.data

        user = Account.objects.get(number=self.transaction_partner_account_number).user

        serialized_data[
            "transaction_partner_name"
        ] = f"{user.first_name} {user.last_name}"
        serialized_data["transaction_partner_account_number"] = int(
            self.transaction_partner_account_number
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serialized_data, status=status.HTTP_201_CREATED, headers=headers
        )


class TransactionDebitCardCreate(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = DebitCardPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    card_owner = None
    transaction_partner_account_number = None

    def perform_create(self, serializer):
        account_number = serializer.validated_data.get("account_number")
        account = Account.objects.filter(number=account_number).first()

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != self.request.user:
            raise exceptions.PermissionDenied("Account does not belong to this user")

        transaction_amount = serializer.validated_data.get("amount")
        card_number = serializer.validated_data.pop("card_number")
        cvv = serializer.validated_data.pop("cvv")
        expiry_date = serializer.validated_data.pop("expiry_date")
        transaction_amount = serializer.validated_data.get("amount")

        # Validation of expiry date
        try:
            month, year = expiry_date.split("/")
            month = int(month)
            year = int(year)

            current_year = int(str(datetime.utcnow().year)[2:])
            current_month = datetime.utcnow().month

            if not (1 <= month <= 12):
                raise DateError("Invalid month")
            elif year < current_year or (
                year == current_year and month < current_month
            ):
                raise DateError("Card has expired")
            elif not (year <= 99):
                raise DateError("Invalid year")
        except DateError as e:
            raise exceptions.PermissionDenied(str(e))
        except ValueError:
            raise exceptions.PermissionDenied("Invalid expiry date")

        def luhn_checksum(card_number):
            digits = [int(x) for x in card_number]
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for digit in even_digits:
                checksum += sum(divmod(digit * 2, 10))
            return checksum % 10

        if luhn_checksum(card_number) != 0:
            raise exceptions.PermissionDenied("Invalid card number")

        card = DebitCard.objects.filter(
            card_number=card_number,
            cvv=cvv,
            expiration_date__year=f'20{year}',
            expiration_date__month=month,
        ).first()


        if not card:
            print(card)
            raise exceptions.PermissionDenied("Invalid card")

        if int(account_number) == int(card.account.number):
            raise exceptions.PermissionDenied(
                "Sender and transaction partner accounts cannot be the same"
            )

        self.transaction_partner_account_number = card.account.number

        if card.account.balance >= transaction_amount:
            serializer.save(transaction_type="DEBIT_CARD", account=account)

            # Update Account Balances
            card.account.balance -= transaction_amount
            account.balance += transaction_amount

            card.account.save()
            account.save()

            # Create Transfer
            transfer = DebitCardTransaction.objects.create(
                transaction=serializer.instance,
                transaction_partner_account=card.account,
            )
        else:
            raise exceptions.PermissionDenied("Insufficient funds")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serialized_data = serializer.data

        user = Account.objects.get(number=self.transaction_partner_account_number).user

        serialized_data[
            "transaction_partner_name"
        ] = f"{user.first_name} {user.last_name}"
        serialized_data["transaction_partner_account_number"] = int(
            self.transaction_partner_account_number
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serialized_data, status=status.HTTP_201_CREATED, headers=headers
        )



class TransactionHistory(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': self.request})

        serialized_data = []

        for data in serializer.data:
            if data is not None:
                serialized_data.append(data)

        return Response(serialized_data, status=status.HTTP_200_OK)
    
class UserTransactionDetail(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "identifier"

    def get_object(self):
        debit_card = Transaction.objects.filter(
            identifier=self.kwargs["identifier"]
        ).first()

        if not debit_card:
            raise exceptions.NotFound()

        return debit_card