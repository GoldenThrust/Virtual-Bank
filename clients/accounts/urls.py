from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('switch-account/<int:pk>/', views.switch_account, name='switch_account'),
    path('create-account/', views.create_account, name='create_account'),
    path('rename-account/', views.rename_account, name='rename_account'),
]