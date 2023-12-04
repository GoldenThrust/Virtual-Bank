from django.shortcuts import render
from django.views.generic import View, TemplateView

class HomePage(TemplateView):
    template_name = "home/index.html"

    def get(self, request):
        return render(request, self.template_name)