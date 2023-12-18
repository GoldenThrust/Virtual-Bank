from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('switch-account/<int:pk>/', views.switch_account, name='switch_account'),
    path('create-account/<int:pk>/', views.switch_account, name='switch_account'),
]