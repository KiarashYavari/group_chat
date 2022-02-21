from django.urls import path
from .consumers import GroupChatConsumer

websocket_urlpatterns = [
    path('ws/group_chat/<slug:group_slug>/',GroupChatConsumer.as_asgi()),
]