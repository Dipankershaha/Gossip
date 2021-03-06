from channels.consumer import SyncConsumer , AsyncConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from App_chat.models import Thread,  Message
from channels.auth import AuthMiddlewareStack
import sys
import json


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        # self.scope["session"].save()
        # print(self.scope['user'])
        # print(self.scope["session"])
        # self.scope["session"].save()
        # sys.exit()

        # me = User.objects.get(username='dipanker')
        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other_username)
        self.thread_obj = Thread.objects.get_or_create_personal_thread(me, other_user)
        self.room_name = f'personal_thread_{self.thread_obj.id}'
        
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send({
            'type':'websocket.accept',
        })
        print(f'[{self.channel_name}] - You are connected')



    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')

        msg = json.dumps({
            'text': event.get('text'),
            'username': self.scope['user'].username,
        })

        # self.store_message(event.get('text'))

        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                'type':'websocket.message',
                'text':msg
            }
        )
        
        # self.send({
        #     'type':'websocket.send',
        #     'text':event.get('text'),
        # })

    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message Sent - {event["text"]}')
        self.send({
            'type':'websocket.send',
            'text':event.get('text'),
        }) 



    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] -  Disconnected')
        print(event)

        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)


    def store_message(self, text):
        Message.objects.create(
            thread = self.thread_obj,
            sender = self.scope['user'],
            text = text

        )


class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        # print("Connect event is called")
        self.room_name = 'broadcast'
        self.send({
            'type':'websocket.accept',
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f'[{self.channel_name}] - You are connected')



    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Received message - {event["text"]}')

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, 
            {
                'type':'websocket.message',
                'text':event.get('text'),
            }
        )
        
        # self.send({
        #     'type':'websocket.send',
        #     'text':event.get('text'),
        # })

    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message Sent - {event["text"]}')
        self.send({
            'type':'websocket.send',
            'text':event.get('text'),
        }) 



    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] -  Disconnected')
        print(event)

        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)