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
from transfers.models import Transfer
from django.db.models import Q, Sum
import requests
from django.contrib.auth import logout

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
import requests


class LoginView(auth_views.LoginView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'login_data' in request.session:
                login_data = request.session.pop('login_data')
                response = requests.post('http://localhost:8000/users/login/', data=login_data)
                
                if response.status_code == 200:
                    cookies = response.cookies

                    redirect_response = redirect("users:dashboard")
                    
                    for key, value in cookies.items():
                        redirect_response.set_cookie(key, value, httponly=True)
                        
                    return redirect_response
                else:
                    logout(request)
                    return redirect("login")
        
        if request.method == "POST":
            request.session['login_data'] = request.POST
        
        return super().dispatch(request, *args, **kwargs)



class RegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get(self, request):
        # if self.request.user.is_authenticated:
        #     return redirect("users:dashboard")

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

            notification_message = (
                f"{user.first_name} {user.last_name} has joined the system"
            )
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

        # processing recent transactions
        if request.session.get("account"):
            recent_transactions = Transaction.objects.filter(
                Q(account=request.session.get("account")["pk"])
                | Q(
                    debit_card__transaction_partner_account=request.session.get(
                        "account"
                    )["pk"]
                )
                | Q(
                    transfer__transaction_partner_account=request.session.get(
                        "account"
                    )["pk"]
                )
            ).order_by("-date")[:10]
            

            financial = {
                "incoming": Transaction.objects.filter(
                    Q(debit_card__transaction__account=request.session.get("account")["pk"])
                    | Q(
                        transfer__transaction_partner_account=request.session.get(
                            "account"
                        )["pk"]
                    )
                    | Q(transaction_type="DEPOSIT", account=request.session.get("account")["pk"])
                ).aggregate(Sum("amount"))["amount__sum"]
                or 0,
                "incoming_2": Transaction.objects.filter(
                    Q(debit_card__transaction__account=request.session.get("account")["pk"])
                    | Q(
                        transfer__transaction_partner_account=request.session.get(
                            "account"
                        )["pk"]
                    )
                ).aggregate(Sum("amount"))["amount__sum"]
                or 0,
                "outgoing": Transaction.objects.filter(
                    Q(
                        debit_card__transaction_partner_account=request.session.get(
                            "account"
                        )["pk"]
                    )
                    | Q(
                        transfer__transaction__account=request.session.get(
                            "account"
                        )["pk"]
                    )
                ).aggregate(Sum("amount"))["amount__sum"]
                or 0,
            }

            # transaction partner
            top_partners = (
                Transfer.objects.filter(
                    transaction__account=request.session.get("account")["pk"]
                )
                .order_by("transaction_partner_account", "-transaction__amount")
                .distinct("transaction_partner_account")[:10]
            )

        else:
            recent_transactions = None
            financial = None
            top_partners = None

        context = {
            "user": request.user,
            "title": "Dashboard",
            "recent_transactions": recent_transactions,
            "financial": financial,
            "top_partners": top_partners,
        }

        return render(request, self.template_name, context)
