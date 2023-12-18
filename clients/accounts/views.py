from django.shortcuts import render, redirect
from .models import Account
from django.views.generic import DetailView
from django.http import JsonResponse
from .utils import update_account
from django.contrib.auth.decorators import login_required
from accounts.utils import generate_account_number

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
                Account.objects.create(
                    user=request.user,
                    name=name,
                    account_type=account_type,
                    currency=currency,
                    number=generate_account_number()
                )
                return JsonResponse({'status': 'success'})
            except Exception as e:
                print(e)
                return JsonResponse({'status': 'failed', 'message': 'Error creating account'})
        
        return JsonResponse({'status': 'failed', 'message': 'Incomplete data'})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})