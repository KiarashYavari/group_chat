from django.urls import path
from .consumers import GroupChat

websocket_urlpatterns = [
    path('ws/group_chat/<slug:group_slug>/',GroupChat.as_asgi()),
]