import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User   
import datetime
from notifications.signals import notify
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f"chat_{self.room_name}"
        #print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
          
    @database_sync_to_async
    def create_chat(self, msg, sender,reciever):
        sender = User.objects.get(username = sender)
        reciever = User.objects.get(username=reciever)
        new_msg = Message.objects.create(sender=sender, reciever=reciever, content=msg)
        new_msg.save()
        notify.send(sender, recipient=reciever, verb='you reached level 10')

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        reciever = text_data_json['reciever']
        new_msg = await self.create_chat(message,sender,reciever)
       # print(message,"messa")
#        print(sender,"senderr")
#        print(reciever,"recieverr")
#        print("-----------------------")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender':sender,
                'reciever': reciever
            })
            
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        #print(event)
        reciever = event['reciever']
        
        # Send message to WebSocket
        #print(new_msg)
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            #'timestamp': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }))