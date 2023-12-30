from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic.edit import FormView
from .forms import UserRegisterForm
from accounts.forms import AccountCreationForm
from accounts.utils import update_account
from .utils import get_client_ip
from django.contrib.auth import views as auth_views
from notifications.utils import process_notifications
from transactions.models import Transaction
from django.db.models import Q
import json


class LoginView(auth_views.LoginView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)

class RegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('users:dashboard')

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.ip_address = get_client_ip(request)
            user.save()
            messages.success(
                request, f"Your account has been created! You are now able to log in"
            )

            notification_message = f"{user.first_name} {user.last_name} has joined the system"
            process_notifications("admin", "user_notification", notification_message)
            return redirect("users:login")
        return render(request, self.template_name, {"form": form})



class DashBoard(View):
    form_class = AccountCreationForm
    template_name = "users/dashboard.html"

    def get(self, request):
        if not request.session.get("account"):
            account = request.user.account_set.first()
            if account:
                update_account(account, request.session)


        update_account(request.session.get("account"), request.session)

        if (request.session.get("account")):
            recent_transactions = Transaction.objects.filter(
                Q(account=request.session.get('account')['pk']) |
                Q(debit_card__transaction_partner_account=request.session.get('account')['pk']) |
                Q(transfer__transaction_partner_account=request.session.get('account')['pk'])).order_by('-date')[:5]
        else:
            recent_transactions = None

        deposit_transactions = Transaction.objects.filter(transaction_type='DEPOSIT', account=request.session.get('account')['pk'])
        transfer_transactions = Transaction.objects.filter(transaction_type='TRANSFER', account=request.session.get('account')['pk'])
        debit_card_transactions = Transaction.objects.filter(transaction_type='DEBIT_CARD', account=request.session.get('account')['pk'])

       # Processing data for the chart
        deposit_data = [{'date': transaction.date.strftime('%Y-%m-%d'), 'amount': float(transaction.amount)} for transaction in deposit_transactions]
        transfer_data = [{'date': transaction.date.strftime('%Y-%m-%d'), 'amount': float(transaction.amount)} for transaction in transfer_transactions]
        debit_card_data = [{'date': transaction.date.strftime('%Y-%m-%d'), 'amount': float(transaction.amount)} for transaction in debit_card_transactions]

        # Convert data to JSON format
        deposit_json = json.dumps(deposit_data)
        transfer_json = json.dumps(transfer_data)
        debit_card_json = json.dumps(debit_card_data)



        context = {
            "title": "Dashboard",
            "recent_transactions": recent_transactions,
            'deposit_data': deposit_json,
            'transfer_data': transfer_json,
            'debit_card_data': debit_card_json,
        }


        return render(request, self.template_name, context)
