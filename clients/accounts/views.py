from django.shortcuts import render, redirect
from .models import Account
from django.views.generic import DetailView
from django.http import HttpResponse
from .utils import update_account
from django.contrib.auth.decorators import login_required

@login_required
def switch_account(request, pk):
    account = Account.objects.filter(pk=pk, user=request.user).first()

    if account:
            update_account(account, request.session)
    return redirect('users:dashboard') 

# @login_required
# def create_account