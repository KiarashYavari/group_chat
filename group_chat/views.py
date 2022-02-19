from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from group_chat.models import GroupChat, Member
from .forms import UserRegisterForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.safestring import mark_safe
import json


# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'group_chat/register.html'
  success_url = reverse_lazy('index')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"

class IndexView(LoginRequiredMixin,ListView):
  template_name = 'group_chat/index.html'
  
  def get_queryset(self):
    current_user = self.request.user
    return current_user.member_set.all()

  context_object_name = 'members'


@login_required
def create_chat(request):
    current_user = request.user
    title = request.POST['group_name']
    new_chat = GroupChat.objects.create(creator=current_user, title=title)
    Member.objects.create(chat=new_chat, user=current_user)
    return redirect(reverse('group_chat:chat', args=[new_chat.group_slug]))


@login_required
def chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(group_slug=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, 'group_chat/404.html')
    if request.method == "GET":
        if Member.objects.filter(chat_id=chat.id, user_id=current_user.id).count() == 0:
            return render(request, 'group_chat/join_chat.html', {'chatObject': chat})

        return render(request, 'group_chat/chat.html', {'chatObject': chat, 'chat_id_json': mark_safe(json.dumps(chat.group_slug))})
    elif request.method == "POST":
        Member.objects.create(chat_id=chat.id, user_id=current_user.id)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.group_slug}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "join", 'username': current_user.username})
            }
        )

        return render(request, 'group_chat/chat.html', {'chatObject': chat, 'chat_id_json': mark_safe(json.dumps(chat.group_slug))})


@login_required
def leave_chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(group_slug=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, 'group_chat/404.html')
    
    if chat.creator_id == current_user.id:
        chat.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.group_slug}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "delete"})
            }
        )

    else:
        Member.objects.filter(chat_id=chat.id, user_id=current_user.id).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.group_slug}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "leave", 'username': current_user.username})
            }
        )

    return redirect('group_chat:index')

