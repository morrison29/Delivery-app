import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from orders.models import Order

from .models import Message


class OrderChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_chat_{self.order_id}'
        user = self.scope['user']

        if not user.is_authenticated:
            await self.close()
            return

        allowed = await self.user_can_access_order(user, self.order_id)
        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        body = data.get('message', '').strip()
        if not body:
            return

        user = self.scope['user']
        message = await self.save_message(user, self.order_id, body)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': body,
                'sender': user.username,
                'sender_id': user.id,
                'created_at': message['created_at'],
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def user_can_access_order(self, user, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return False
        return user.is_delivery_agent or order.customer_id == user.id

    @database_sync_to_async
    def save_message(self, user, order_id, body):
        msg = Message.objects.create(order_id=order_id, sender=user, body=body)
        return {'created_at': msg.created_at.strftime('%H:%M')}
