from django.shortcuts import render, redirect
from .models import Account
from django.views.generic import DetailView
from django.http import JsonResponse, Http404
from .utils import update_account
from django.contrib.auth.decorators import login_required
from .utils import generate_account_number

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
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'message': 'Error renaming account'})
            
        return JsonResponse({'status': 'failed', 'message': 'Error processing data'})
    raise Http404()