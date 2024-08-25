from django.urls import re_path
from .consumers import TransactionConsumer

websocket_urlpatterns = [
    re_path(r'ws/transactions/$', TransactionConsumer.as_asgi()),
]
