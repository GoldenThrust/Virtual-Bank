from django.urls import re_path
from .consumers import Consumer

websocket_urlpatterns = [
    re_path(r'ws/socket/$', Consumer.as_asgi()),
]
