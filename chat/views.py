from django.shortcuts import HttpResponse
from django.views.generic.base import TemplateView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your views here.
class ChatView(TemplateView):
    template_name = "chat/chatview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def chat_new_message(request, sender):
    receiver = request.GET['receiver']
    text = request.GET['text']
    group_name = f"chat_{receiver}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
                {
                    'type': 'chat_message',
                    'message': {'sender': sender, 'receiver': receiver, 'text': text}
                }
    )

    return HttpResponse('message sent!')
