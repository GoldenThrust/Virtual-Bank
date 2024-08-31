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
from django.db.models import Q, Sum
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from utils.constant import api_url
import requests


class LoginView(auth_views.LoginView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if "login_data" in request.session:
                cookies = request.COOKIES
                requests.get(f"{api_url}auth/logout", cookies=cookies)
                login_data = request.session.pop("login_data")
                response = requests.post(f"{api_url}auth/login/", data=login_data)

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
            request.session["login_data"] = request.POST

        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect("users:dashboard")

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)  # Include request.FILES
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
                | Q(payer=request.session.get("account")["pk"])
                | Q(
                    payee=request.session.get(
                        "account"
                    )["pk"]
                )
            ).order_by("-date")[:10]

            financial = {
                "incoming": Transaction.objects.filter(
                    payee=request.session.get("account")["pk"]
                ).aggregate(Sum("amount_received"))["amount_received__sum"]
                or 0,
                "incoming_2": Transaction.objects.filter(
                    ~Q(transaction_type="DEPOSIT"),
                    payee=request.session.get("account")["pk"],
                ).aggregate(Sum("amount_received"))["amount_received__sum"]
                or 0,
                "outgoing": Transaction.objects.filter(
                        ~Q(transaction_type="DEPOSIT"),
                        payer=request.session.get("account")[
                            "pk"
                        ]
                ).aggregate(Sum("amount_sent"))["amount_sent__sum"]
                or 0,
            }

            # transaction partner
            top_partners = (
                Transaction.objects.filter(transaction_type="TRANSFER")
                .order_by("-amount_sent")
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


class LogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        cookies = request.COOKIES
        requests.get(f"{api_url}auth/logout", cookies=cookies)
        response = super().dispatch(request, *args, **kwargs)

        response.delete_cookie("vb_token")

        response.delete_cookie("vb_rtoken")

        return response
