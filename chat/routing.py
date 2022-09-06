# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<room>/', consumers.ChatConsumer.as_asgi()),
]