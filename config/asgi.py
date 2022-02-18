"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from echo.routing import websocket_urlpatterns as echo_routing
from chat.routing import websocket_urlpatterns as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,

    "websocket" : AuthMiddlewareStack(
        URLRouter([
              path('',URLRouter(chat_routing)),
              path('',URLRouter(echo_routing)),
        ]
        ),
    ),
})
