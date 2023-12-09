from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic.edit import FormView
from .forms import UserRegisterForm


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
        return render(request, self.template_name, {'title': 'Dashboard'})