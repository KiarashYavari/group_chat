from django.urls import path
from .consumers import EchoConsumer

websocket_urlpatterns =([
    path('ws/echo', EchoConsumer.as_asgi()),
    path('ws/echo/image', EchoConsumer.as_asgi()),
])