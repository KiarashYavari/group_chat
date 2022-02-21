from channels.generic.websocket import AsyncJsonWebsocketConsumer

class GroupChat(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_slug']
        self.room_name = 'chat_%s' % self.group_id
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, content=None):
        if content != None:
            text = content.get('text')
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'group_chat_message',
                    'message': {'type': "msg", 'text': text},
                    'sender' : self.channel_name
                }
            )


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )


    async def group_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        if self.channel_name != sender:
            await self.send_json(content=message)

    
    async def group_chat_activity(self, event):
        message = event['message']
        await self.send_json(content=message)