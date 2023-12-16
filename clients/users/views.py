from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic.edit import FormView
from .forms import UserRegisterForm
from django.core.serializers import serialize
import json
class RegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Your account has been created! You are now able to log in"
            )
            return redirect("users:login")
        return render(request, self.template_name, {"form": form})



class DashBoard(View):
    template_name = "users/dashboard.html"

    def get(self, request):
        # if not request.session.get("account"):
        account = request.user.account_set.first()
        if account:
            serialized_account = serialize('json', [account])
            deserialized_account = json.loads(serialized_account)
            request.session["account"] = deserialized_account[0]['fields']

        return render(request, self.template_name, {'title': 'Dashboard'})
