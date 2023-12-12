from rest_framework import generics
from datetime import datetime
from notifications.utils import process_notifications
from django.utils.timezone import localtime
from debit_cards.utils import luhn_checksum

# Models and Serializers
from .models import Transaction
from accounts.models import Account
from deposits.models import Deposit

# from payments.models import Payment
from transfers.models import Transfer
from .serializers import (
    TransactionSerializer,
    TransferTransactionSerializer,
    DebitCardPaymentSerializer,
    TransactionHistorySerializer,
)
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
        
        # notification
        notification_message = f"A deposit of {transaction_amount} has been credited to your account ({account_number})."
        process_notifications(
            self.request.user, "transaction_notification", notification_message
        )


class TransactionTransferCreate(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransferTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    transaction_partner_account_number = None

    def perform_create(self, serializer):
        account_number = serializer.validated_data.get("account_number")
        account = Account.objects.filter(number=account_number).first()
        user = self.request.user
        user_name = f"{user.first_name} {user.last_name}"

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != user:
            # account.user.is_active = False
            # account.user.save()

            # notification
            notification_message = f"{user_name} attempted a transfer using your account ({account.number}). For security purposes, the action has been flagged."
            process_notifications(account.user, "security_notification", notification_message)
            raise exceptions.PermissionDenied("Account does not belong to this user")


        transaction_amount = serializer.validated_data.get("amount")
        self.transaction_partner_account_number = serializer.validated_data.pop(
            "transaction_partner_account_number"
        )

        if int(account_number) == int(self.transaction_partner_account_number):
            # notification
            notification_message = "The transfer could not be completed."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            raise exceptions.PermissionDenied(
                "Sender and transaction partner accounts cannot be identical."
            )

        transaction_partner_account = Account.objects.filter(
            number=self.transaction_partner_account_number
        ).first()

        if not transaction_partner_account:
            # notification
            notification_message = "The transfer could not be completed due to an invalid transaction partner account number."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )
            raise exceptions.NotFound("Transaction partner Account not found")

        if account.balance >= transaction_amount:
            transaction_partner_account_name = f'{transaction_partner_account.user.first_name} {transaction_partner_account.user.last_name}'
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
        
            # notification
            notification_message = f"The transfer of {transaction_amount} to {transaction_partner_account_name}'s account was successful."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            # notification
            notification_message = f"{user_name} has sent {transaction_amount} to your account ({transaction_partner_account.number})."
            process_notifications(
                transaction_partner_account.user, "transaction_notification", notification_message
            )
        else:
            # notification
            notification_message = "The transfer could not be completed due to insufficient funds."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )
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
        user = self.request.user
        user_name = f"{user.first_name} {user.last_name}"

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
        
        # validate card number using luhn algorithm
        if luhn_checksum(card_number) != 0:
            raise exceptions.PermissionDenied("Invalid card number")

        card = DebitCard.objects.filter(
            card_number=card_number,
            cvv=cvv,
            expiration_date__year=f"20{year}",
            expiration_date__month=month,
        ).first()

        if not card:
            print(card)
            raise exceptions.PermissionDenied("Invalid card")

        if int(account_number) == int(card.account.number):
            #notification
            notification_message = "The debit card transaction could not be completed."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            raise exceptions.PermissionDenied(
                "Sender and transaction partner accounts cannot be the same"
            )

        self.transaction_partner_account_number = card.account.number

        if card.account.balance >= transaction_amount:
            transaction_partner_account_name = f'{card.account.user.first_name} {card.acount.user.last_name}'
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

                    
            # notification
            notification_message = f"You've successfully initiated a debit card transaction. {transaction_amount} was debited from your account and sent to {user_name}'s account."
            process_notifications(
                card.account.user, "transaction_notification", notification_message
            )

            # notification
            notification_message = f"You've received {transaction_amount} from {transaction_partner_account_name} through a debit card transaction."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )
        else:
            # notification
            notification_message = f"The debit card transaction from {user_name} could not be completed due to insufficient funds in their account."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            # notification
            notification_message = "Your debit card transaction couldn't be completed due to insufficient funds."
            process_notifications(
                card.account.user, "transaction_notification", notification_message
            )
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
        serializer = self.serializer_class(
            queryset, many=True, context={"request": self.request}
        )

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
        peek_user = self.request.user
        transaction = Transaction.objects.filter(identifier=self.kwargs["identifier"]).first()

        if not transaction:
            raise exceptions.NotFound()

        transaction_partner = None
        if transaction.account.user != peek_user:
            if transaction.transaction_type in ['TRANSFER', 'DEBIT_CARD']:
                transaction_partner = transaction.transfer.transaction_partner_account.user if transaction.transaction_type == 'TRANSFER' else transaction.debit_card.transaction_partner.user

            transaction_date = localtime(transaction.date).strftime('%m/%d/%Y at %I:%M %p')
            user_name = 'Virtual-Bank administrator' if peek_user.is_superuser else f'{peek_user.first_name} {peek_user.last_name}'

            # notification
            notification_message = f'{user_name} reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(transaction.account.user, 'security_notification', notification_message)

            if transaction_partner and transaction_partner != peek_user:
                process_notifications(transaction_partner, 'security_notification', notification_message)

        return transaction
