from django.urls import path

from . import views

app_name = 'transactions'

urlpatterns = [
    path('transactions_chart/', views.transactions_chart_data, name='transactions_chart'),
]