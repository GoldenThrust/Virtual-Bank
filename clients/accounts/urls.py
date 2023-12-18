from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('switch-account/<int:pk>/', views.SwitchAccountView.as_view(), name='switch_account'),
]