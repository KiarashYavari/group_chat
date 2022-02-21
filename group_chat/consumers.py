from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import GroupChat, Message

class GroupChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_slug']
        self.current_user = self.scope['user']
        self.group_chat_obj = await self.get_group_chat_obj(group_slug=self.group_id)
        if self.group_chat_obj:
            self.room_name = 'chat_%s' % self.group_id
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()


    async def receive_json(self, content=None):
        if content != None:
            text = content.get('text')
            await self.create_message_obj(author=self.current_user, text = text, group_chat_obj= self.group_chat_obj)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'group_chat_message',
                    'message': {'type': "msg", 'sender':self.current_user.username, 'text': text},
                    'sender_channel_name' : self.channel_name
                }
            )


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )


    async def group_chat_message(self, event):
        message = event['message']
        sender = event['sender_channel_name']
        if self.channel_name != sender:
            await self.send_json(content=message)

    
    async def group_chat_activity(self, event):
        message = event['message']
        await self.send_json(content=message)


    @database_sync_to_async
    def get_group_chat_obj(self, group_slug):
        try:
            group_chat_obj = GroupChat.objects.get(group_slug = group_slug)
            return group_chat_obj
        except GroupChat.DoesNotExist:
            return None
        

    @database_sync_to_async
    def create_message_obj(self, author, text, group_chat_obj):
        Message.objects.create(author=author, text_content=text, msg_group_chat=group_chat_obj)
