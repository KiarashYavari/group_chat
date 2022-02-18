from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.

#group_chats, member, message
def auto_generate_str(length=15):
    source = "abcdefghijklmnopqrztuvwxyz"
    result = ""
    for _ in range(length):
        result += source[random.randint(0, length)]
    return result


class GroupChat(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    group_slug = models.SlugField(unique=True, max_length=200, default=auto_generate_str())


class Member(models.Model):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    msg_group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    text_content = models.TextField()
    msg_created_date = models.DateTimeField(auto_now_add=True)