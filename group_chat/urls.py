from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from group_chat.views import IndexView, SignUpView, create_chat, chat, leave_chat



app_name = 'group_chat'

urlpatterns = [
    path('accounts/register/', SignUpView.as_view(), name='register'),
    path('accounts/login/',LoginView.as_view(template_name='group_chat/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='group_chat/logout.html'), name='logout'),
    path('group_chat/', IndexView.as_view(), name='index'),
    path('create/', create_chat, name='create_chat'),
    path('<str:chat_id>/', chat, name='chat'),
    path('<str:chat_id>/leave/', leave_chat, name='leave_chat'),
]