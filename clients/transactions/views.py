from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse

# Models and Serializers
from .models import Transaction
import json


def transactions_chart_data(request):
        deposit_transactions = Transaction.objects.filter(transaction_type='DEPOSIT', account=request.session.get('account')['pk'])
        transfer_transactions = Transaction.objects.filter(transaction_type='TRANSFER', account=request.session.get('account')['pk'])
        debit_card_transactions = Transaction.objects.filter(transaction_type='DEBIT_CARD', account=request.session.get('account')['pk'])

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