import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Check if user is logged in
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        # Join the channel layer group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # (Optional) Load recent messages from DB (e.g., last 50)
        messages = await sync_to_async(list)(
            ChatMessage.objects.filter(room_name=self.room_name).order_by('-timestamp')[:50]
        )
        # Send them in reverse order so oldest appear first
        for msg in reversed(messages):
            await self.send(text_data=json.dumps({
                'message': f"{msg.user.username}: {msg.content}"
            }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        user = self.scope["user"]

        if not user.is_authenticated:
            return  # ignore messages from unauthenticated user

        # Store message in DB
        await sync_to_async(ChatMessage.objects.create)(
            user=user,
            room_name=self.room_name,
            content=message,
            timestamp=timezone.now()
        )

        # Broadcast the message to everyone in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': user.username,
                'message': message
            }
        )

    async def chat_message(self, event):
        # This method is called for each broadcast
        username = event.get('username', 'Anonymous')
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': f"{username}: {message}"
        }))

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
