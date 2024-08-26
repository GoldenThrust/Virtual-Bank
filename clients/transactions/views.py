from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
# Models
from .models import Transaction
from itertools import chain


def transactions_chart_data(request):
    deposit_transactions = Transaction.objects.filter(
        transaction_type="DEPOSIT", account=request.session.get("account")["pk"]
    )
    transfer_transactions = Transaction.objects.filter(
        Q(account=request.session.get("account")["pk"])
        | Q(transfer__transaction_partner_account=request.session.get("account")["pk"]),
        transaction_type="TRANSFER",
    )
    debit_card_transactions = Transaction.objects.filter(
        Q(account=request.session.get("account")["pk"])
        | Q(
            debit_card__transaction_partner_account=request.session.get("account")["pk"]
        ),
        transaction_type="DEBIT_CARD",
    )

    user_id = request.session.get("account")["user"]
    format_date = lambda transaction: transaction.date.strftime("%Y-%m-%dT%H:%M:%S")
    format_amount = lambda transaction: float(transaction.amount)

    def get_payer_and_payee(transaction):
        payer = (
            "You"
            if user_id == transaction.account.user.pk
            else transaction.account.user.get_full_name()
        )
        payee = (
            "You"
            if user_id != transaction.account.user.pk
            else transaction.account.user.get_full_name()
        )

        if transaction.transaction_type == "TRANSFER":
            if user_id == transaction.account.user.pk:
                if hasattr(transaction, "transfer"):
                    payee = (
                        transaction.transfer.transaction_partner_account.user.get_full_name()
                    )
                else:
                    payee = "Unknown"
            else:
                payer = transaction.account.user.get_full_name()
        elif transaction.transaction_type == "DEBIT_CARD":
            if user_id == transaction.account.user.pk:
                payer = transaction.account.user.get_full_name()
            else:
                if hasattr(transaction, "debit_card"):
                    payee = (
                        transaction.debit_card.transaction_partner_account.user.get_full_name()
                    )
                else:
                    payee = "Unknown"

        return payer, payee

    deposit_data = [
        {"date": format_date(t), "amount": format_amount(t)}
        for t in deposit_transactions
    ]

    transfer_data = [
        {
            "date": format_date(t),
            "amount": format_amount(t),
            "payer": get_payer_and_payee(t)[0],
            "payee": get_payer_and_payee(t)[1],
        }
        for t in transfer_transactions
    ]

    debit_card_data = [
        {
            "date": format_date(t),
            "amount": format_amount(t),
            "payer": get_payer_and_payee(t)[0],
            "payee": get_payer_and_payee(t)[1],
        }
        for t in debit_card_transactions
    ]

    data = {
        "deposit_data": deposit_data,
        "transfer_data": transfer_data,
        "debit_card_data": debit_card_data,
    }

    return JsonResponse(data)
