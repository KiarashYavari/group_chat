from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_name = 'chat_%s' % self.username
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, content=None):
        if content != None:
            username = content.get('receiver')
            user_group_name = f"chat_{username}"
            
            await self.channel_layer.group_send(
                user_group_name,
                {
                    'type': 'chat_message',
                    'message': content
                }
            )


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )


    async def chat_message(self, event):
        message = event['message']
        await self.send_json(content=message)