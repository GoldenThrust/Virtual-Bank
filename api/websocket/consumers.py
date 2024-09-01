from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        print(self.user)
        
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            
            self.send()
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

    async def send_transaction(self, event):
        data = event['data']
        
        await self.send(text_data=json.dumps({
            'content': data,
            'type': 'transaction'
        }))
        
    async def send_notification(self, event):
        message = event['data']
        
        await self.send(text_data=json.dumps({
            'content': message,
            'type': 'notification'
        }))