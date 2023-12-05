from django.shortcuts import render
from django.views.generic import View, TemplateView

class HomePage(TemplateView):
    template_name = "home/index.html"

class AboutPage(TemplateView):
    template_name = "home/about.html"