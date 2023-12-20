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

        return render(request, self.template_name, {'title': 'Dashboard'})
