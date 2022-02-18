from django.urls import path
from .views import ChatView, chat_new_message

urlpatterns = [
    path('chat/<slug:username>', ChatView.as_view(), name="chat"),
    path('chat/new/<slug:sender>/', chat_new_message, name='chat_new_message')
]
