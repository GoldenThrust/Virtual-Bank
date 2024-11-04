from rest_framework import generics
from datetime import datetime
from notifications.utils import process_notifications
from django.utils.timezone import localtime
from debit_cards.utils import luhn_checksum
from django.db.models import Q

# Models and Serializers
from .models import Transaction
from accounts.models import Account

from .serializers import (
    TransactionSerializer,
    TransferSerializer,
    DebitCardTransactionSerializer,
    DepositSerializer
)
from debit_cards.models import DebitCard

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import exceptions
from .utils import convert_currency
from accounts.utils import currency_to_unicode

from .paginations import TransactionPagination

class DateError(Exception):
    pass


class TransactionListAdmin(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = TransactionPagination


class TransactionDetailAdmin(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]


class CreateDepositTransaction(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account_number = serializer.validated_data.pop("account_number")
        transaction_amount = serializer.validated_data.pop("amount")
        account = Account.objects.filter(number=account_number).first()

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != self.request.user:
            raise exceptions.PermissionDenied("Account does not belong to this user")

        serializer.save(account=account, payer=account, payee=account, amount_sent=transaction_amount, amount_received=transaction_amount, transaction_type="DEPOSIT", currency_sent=account.currency, currency_received=account.currency, rate=1)

        # Update Account Balance
        account.balance += transaction_amount
        account.save()

        # notification
        notification_message = f"A deposit of {transaction_amount} has been credited to your account ({account_number})."
        process_notifications(
            self.request.user, "transaction_notification", notification_message
        )


class CreateTransferTransaction(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payer_account_number = serializer.validated_data.pop("payer_account_number")
        payee_account_number = serializer.validated_data.pop("payee_account_number")
        transaction_amount = serializer.validated_data.pop("amount")

        account = Account.objects.filter(number=payer_account_number).first()
        user = self.request.user
        user_name = f"{user.first_name} {user.last_name}"

        if int(payer_account_number) == int(payee_account_number):
            # notification
            notification_message = "The transfer could not be completed."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            raise exceptions.PermissionDenied(
                "Payer and Payee accounts cannot be identical."
            )

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != user:
            # notification
            notification_message = f"{user_name} attempted a transfer using your account ({account.number}). For security purposes, the action has been flagged."
            process_notifications(
                account.user, "security_notification", notification_message
            )
            raise exceptions.PermissionDenied("Account does not belong to this user")

        payee_account = Account.objects.filter(number=payee_account_number).first()

        if not payee_account:
            # notification
            notification_message = (
                "The transfer could not be completed due to an invalid account number."
            )
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )
            raise exceptions.NotFound("Payee Account not found")

        if account.balance >= transaction_amount:
            payee_account_name = payee_account.user.get_full_name()
            currency = convert_currency(
                transaction_amount, account.currency, payee_account.currency
            )
            received_amount = currency[0]
            rate = currency[1] / currency[2]

            # Update Account Balances
            account.balance -= transaction_amount
            payee_account.balance += received_amount

            account.save()
            payee_account.save()

            serializer.save(
                account=account,
                payer=account,
                payee=payee_account,
                amount_sent=transaction_amount,
                amount_received=received_amount,
                currency_sent=account.currency,
                currency_received=payee_account.currency,
                rate=rate,
                transaction_type="TRANSFER"
            )

            if self.request.user == payee_account.user:
                notification_message = f"The transfer of {currency_to_unicode(account.currency)}{transaction_amount} to {account.name} was successful."
                process_notifications(
                    self.request.user, "transaction_notification", notification_message
                )
            else:
                # notification
                notification_message = f"The transfer of {currency_to_unicode(account.currency)}{transaction_amount} to {payee_account_name}'s account was successful."
                process_notifications(
                    self.request.user, "transaction_notification", notification_message
                )

                # notification
                notification_message = f"{user_name} has sent {currency_to_unicode(account.currency)}{transaction_amount} to your account ({payee_account.number})."
                process_notifications(
                    payee_account.user, "transaction_notification", notification_message
                )

        else:
            # notification
            notification_message = (
                "The transfer could not be completed due to insufficient funds."
            )
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )
            raise exceptions.PermissionDenied("Insufficient funds")


class CreateDebitCardTransaction(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = DebitCardTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account_number = serializer.validated_data.pop("payee_account_number")
        card_number = serializer.validated_data.pop("card_number")
        cvv = serializer.validated_data.pop("cvv")
        expiration_date = serializer.validated_data.pop("expiration_date")

        transaction_amount = serializer.validated_data.pop("amount")


        account = Account.objects.filter(number=account_number).first()
        user = self.request.user
        user_name = f"{user.first_name} {user.last_name}"

        if not account:
            raise exceptions.NotFound("Account not found")

        if account.user != self.request.user:
            raise exceptions.PermissionDenied("Account does not belong to this user")

        # Validation of expiry date
        try:
            month, year = expiration_date.split("/")
            month = int(month)
            year = int(year)

            current_year = int(str(datetime.now().year)[2:])
            current_month = int(datetime.now().month)

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
            raise exceptions.PermissionDenied("Invalid card")

        if int(account_number) == int(card.account.number):
            # notification
            notification_message = "The debit card transaction could not be completed."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            raise exceptions.PermissionDenied(
                "Payee and Payer accounts cannot be the same"
            )

        payer_account = card.account
        payer_account_name = card.account.user.get_full_name()
        if card.account.balance >= transaction_amount:
            currency = convert_currency(
                transaction_amount, payer_account.currency, account.currency
            )
            received_amount = currency[0]
            rate = currency[1] / currency[2]
            
            # Update Account Balances
            card.account.balance -= transaction_amount
            account.balance += currency[0]

            card.account.save()
            account.save()

            serializer.save(
                account=account,
                payer=payer_account,
                payee=account,
                amount_sent=transaction_amount,
                amount_received=received_amount,
                currency_sent=payer_account.currency,
                currency_received=account.currency,
                rate=rate,
                transaction_type="DEBIT_CARD"
            )

            if self.request.user == card.account.user:
                notification_message = f"You've successfully initiated a debit card transaction. {currency_to_unicode(card.account.currency)}{transaction_amount} was debited from your account and sent to {card.account.name} account."
                process_notifications(
                    self.request.user, "transaction_notification", notification_message
                )
            else:
                # notification
                notification_message = f"You've successfully initiated a debit card transaction. {currency_to_unicode(card.account.currency)}{transaction_amount} was debited from your account and sent to {user_name}'s account."
                process_notifications(
                    card.account.user, "transaction_notification", notification_message
                )

                # notification
                notification_message = f"You've received {currency_to_unicode(card.account.currency)}{transaction_amount} from {payer_account_name} through a debit card transaction."
                process_notifications(
                    self.request.user, "transaction_notification", notification_message
                )
        else:
            # notification
            notification_message = f"The debit card transaction from {payer_account_name} could not be completed due to insufficient funds in their account."
            process_notifications(
                self.request.user, "transaction_notification", notification_message
            )

            # notification
            notification_message = "Your debit card transaction couldn't be completed due to insufficient funds."
            process_notifications(
                card.account.user, "transaction_notification", notification_message
            )
            raise exceptions.PermissionDenied("Insufficient funds")


class TransactionHistory(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TransactionPagination


    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role', None)
        account_number = self.request.query_params.get('account_number', None)

        queryset = Transaction.objects.all()

        if role == "payer":
            queryset = queryset.filter(payer__user=user)
            if account_number:
                queryset = queryset.filter(payer__number=account_number)
        elif role == "payee":
            queryset = queryset.filter(payee__user=user)
            if account_number:
                queryset = queryset.filter(payee__number=account_number)
        else:
            queryset = queryset.filter(
                Q(account__user=user) |
                Q(payer__user=user) |
                Q(payee__user=user)
            )
            if account_number:
                queryset = queryset.filter(
                    Q(account__number=account_number) |
                    Q(payer__number=account_number) |
                    Q(payee__number=account_number)
                )
                

        return queryset

class TransactionDetail(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "identifier"

    def get_object(self):
        user = self.request.user
        transaction = Transaction.objects.filter(
            identifier=self.kwargs["identifier"]
        ).first()

        if not transaction:
            raise exceptions.NotFound()

        if (
            transaction.account != user
            or transaction.payer != user
            or transaction.payee != user
        ):
            transaction_date = localtime(transaction.date).strftime(
                "%m/%d/%Y at %I:%M %p"
            )
            user_name = (
                "Virtual-Bank administrator"
                if user.is_superuser
                else f"{user.first_name} {user.last_name}"
            )

            # notification
            notification_message = f'{user_name} reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(
                transaction.account.user, "security_notification", notification_message
            )

        return transaction


class DepositList(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TransactionPagination

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(account__user=user, transaction_type="DEPOSIT")


class DepositDetail(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "identifier"

    def get_object(self):
        deposit = Transaction.objects.filter(
            identifier=self.kwargs["identifier"], transaction_type="DEPOSIT"
        ).first()

        if not deposit:
            raise exceptions.NotFound()

        if self.request.user != deposit.account.user:
            user = self.request.user
            transaction_date = localtime(deposit.transaction.date).strftime(
                "%m/%d/%Y at %I:%M %p"
            )
            user_name = f"{user.first_name} {user.last_name}"
            if user.is_superuser:
                user_name = "Virtual-Bank administrator"

            # notification
            notification_message = f'{user_name} reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(
                deposit.transaction.account.user,
                "security_notification",
                notification_message,
            )
        return deposit

class TransferHistory(generics.ListAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TransactionPagination

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role', None)
        account_number = self.request.query_params.get('account_number', None)

        queryset = Transaction.objects.filter(transaction_type="TRANSFER")

        if role == "payer":
            queryset = queryset.filter(payer__user=user)
            if account_number:
                queryset = queryset.filter(payer__number=account_number)
        elif role == "payee":
            queryset = queryset.filter(payee__user=user)
            if account_number:
                queryset = queryset.filter(payee__number=account_number)
        else:
            queryset = queryset.filter(
                Q(account__user=user) |
                Q(payer__user=user) |
                Q(payee__user=user)
            )
            if account_number:
                queryset = queryset.filter(
                    Q(account__number=account_number) |
                    Q(payer__number=account_number) |
                    Q(payee__number=account_number)
                )
        

        return queryset


class TransferDetails(generics.RetrieveAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        transfer = Transaction.objects.filter(
            identifier=self.kwargs["identifier"], transaction_type="TRANSFER"
        ).first()

        if not transfer:
            raise exceptions.NotFound()

        payer = transfer.payer.user
        payee = transfer.payee.user
        if (
            self.request.user != payer
            and self.request.user != payee
        ):
            user = self.request.user
            transaction_date = localtime(transfer.transaction.date).strftime(
                "%m/%d/%Y at %I:%M %p"
            )
            user_name = f"{user.first_name} {user.last_name}"
            if user.is_superuser:
                user_name = "Virtual-Bank administrator"

            # notification
            notification_message = f'{user_name} reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(
                payer, "security_notification", notification_message
            )
            process_notifications(
                payee, "security_notification", notification_message
            )

        return transfer



class DebitCardHistory(generics.ListAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TransactionPagination

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role', None)
        account_number = self.request.query_params.get('account_number', None)

        queryset = Transaction.objects.filter(transaction_type="DEBIT_CARD")

        if role == "payer":
            queryset = queryset.filter(payer__user=user)
            if account_number:
                queryset = queryset.filter(payer__number=account_number)
        elif role == "payee":
            queryset = queryset.filter(payee__user=user)
            if account_number:
                queryset = queryset.filter(payee__number=account_number)
        else:
            queryset = queryset.filter(
                Q(account__user=user) |
                Q(payer__user=user) |
                Q(payee__user=user)
            )
            if account_number:
                queryset = queryset.filter(
                    Q(account__number=account_number) |
                    Q(payer__number=account_number) |
                    Q(payee__number=account_number)
                )
                
        return queryset


class DebitCardDetails(generics.RetrieveAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        card = Transaction.objects.filter(
            identifier=self.kwargs["identifier"], transaction_type="DEBIT_CARD"
        ).first()

        if not card:
            raise exceptions.NotFound()

        payer = card.payer.user
        payee = card.payee.user
        if (
            self.request.user != payer
            and self.request.user != payee
        ):
            user = self.request.user
            transaction_date = localtime(card.transaction.date).strftime(
                "%m/%d/%Y at %I:%M %p"
            )
            user_name = f"{user.first_name} {user.last_name}"
            if user.is_superuser:
                user_name = "Virtual-Bank administrator"

            # notification
            notification_message = f'{user_name} reviewed the transaction ({self.kwargs["identifier"]}) that was initiated on {transaction_date}.'
            process_notifications(
                payer, "security_notification", notification_message
            )
            process_notifications(
                payee, "security_notification", notification_message
            )

        return card

