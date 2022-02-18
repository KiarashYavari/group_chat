from django.urls import path
from .consumers import ChatConsumers

websocket_urlpatterns = [
    path('ws/chat/<slug:username>/', ChatConsumers.as_asgi()),
]