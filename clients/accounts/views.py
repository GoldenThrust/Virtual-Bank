from django.shortcuts import render, redirect
from .models import Account
from django.views.generic import DetailView
from django.http import JsonResponse, Http404
from .utils import update_account
from django.contrib.auth.decorators import login_required
from .utils import generate_account_number
from notifications.models import Notification
from notifications.utils import process_notifications
from debit_cards.models import DebitCard
from debit_cards.utils import generate_valid_credit_card_number, generate_cvv
import datetime

@login_required
def switch_account(request, pk):
    account = Account.objects.filter(pk=pk, user=request.user).first()

    if account:
            update_account(account, request.session)
    return redirect('users:dashboard') 


def create_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account_type = request.POST.get('account_type')
        currency = request.POST.get('currency')

        existing_account = Account.objects.filter(user=request.user, name=name).exists()

        if existing_account:
            return JsonResponse({'status': 'failed', 'message': 'Account with this name already exists for the user'})


        if name and account_type and currency:
            try:
                account = Account.objects.create(
                    user=request.user,
                    name=name,
                    account_type=account_type,
                    currency=currency,
                    number=generate_account_number()
                )

                update_account(account, request.session)

                notification_message  = f'A new Account ({account.number}) has been successfully created.'
                process_notifications(request.user, 'account_notification', notification_message)

                if account_type == "CURRENT":
                    debit_card = DebitCard(account=account)
                    card_number = generate_valid_credit_card_number()
                    expiry_date = datetime.datetime.now() + datetime.timedelta(days=365 * 3)
                    debit_card.card_number = card_number
                    debit_card.cvv = generate_cvv(card_number, expiry_date)
                    debit_card.expiration_date = expiry_date
                    debit_card.save()

                    # notification
                    notification_message = f'A debit card has been successfully created for your account ({account.number}).'
                    process_notifications(request.user, 'account_notification', notification_message)
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'message': 'Error creating account'})

        return JsonResponse({'status': 'failed', 'message': 'Error processing data'})
    raise Http404()

def rename_account(request):
    if request.method == 'POST':
        id =   request.POST.get('id')
        name = request.POST.get('name')

        existing_account = Account.objects.filter(user=request.user, name=name).exists()

        if existing_account:
            return JsonResponse({'status': 'failed', 'message': 'Account with this name already exists for the user'})
        
        if id and name:
            try:
                account = Account.objects.get(
                    pk=id,
                    user=request.user,
                )

                account.name = name
                account.save()

                update_account(account, request.session)

                notification_message = f"Your account ({account.number}) has been successfully renamed to {name}."

                process_notifications(request.user, 'account_notification', notification_message)
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'message': 'Error renaming account'})
            
        return JsonResponse({'status': 'failed', 'message': 'Error processing data'})
    raise Http404()