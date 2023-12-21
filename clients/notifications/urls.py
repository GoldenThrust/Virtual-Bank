from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('read-notification/<int:pk>/', views.read_notification, name='read_notification'),
]