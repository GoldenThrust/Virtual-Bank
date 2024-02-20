from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
# Models
from .models import Transaction


def transactions_chart_data(request):
        deposit_transactions = Transaction.objects.filter(transaction_type='DEPOSIT', account=request.session.get('account')['pk'])
        transfer_transactions = Transaction.objects.filter(Q(account=request.session.get('account')['pk'])
                                                            | Q(transfer__transaction_partner_account=request.session.get("account")["pk"]), transaction_type='TRANSFER',  )
        debit_card_transactions = Transaction.objects.filter(Q(account=request.session.get('account')['pk'])
                                                            | Q(debit_card__transaction_partner_account=request.session.get("account")["pk"]), transaction_type='DEBIT_CARD')

       # Processing data for the chart
        deposit_data = [{'date': transaction.date.strftime('%Y-%m-%d'), 'amount': float(transaction.amount)} for transaction in deposit_transactions]
        transfer_data = [{'date': transaction.date.strftime('%Y-%m-%d'), 'amount': float(transaction.amount)} for transaction in transfer_transactions]
        debit_card_data = [{'date': transaction.date.strftime('%Y-%m-%d'), 'amount': float(transaction.amount)} for transaction in debit_card_transactions]

        # Convert data to JSON format
        deposit_json = deposit_data
        transfer_json = transfer_data
        debit_card_json = debit_card_data


        data = {
            'deposit_data': deposit_json,
            'transfer_data': transfer_json,
            'debit_card_data': debit_card_json,
        }

        return JsonResponse(data)