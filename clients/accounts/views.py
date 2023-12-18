from django.shortcuts import render, redirect
from .models import Account
from django.views.generic import DetailView
from django.http import HttpResponse
from .utils import update_account

class SwitchAccountView(DetailView):
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            account = request.user.account_set.get(pk=self.kwargs.get('pk'))
        except Account.DoesNotExist:
            return redirect('users:dashboard')


        if account:
            update_account(account, request.session)
        return redirect('users:dashboard') # Todo - change logic
    

# def switch_account_view(request):
    # accounts = request.user.account_set

    # for account in accounts:
    #     if account.id = request.pk

    # if account:
    #     serialized_account = serialize('json', [account])
    #     deserialized_account = json.loads(serialized_account)
    #     request.session["account"] = deserialized_account[0]['fields']