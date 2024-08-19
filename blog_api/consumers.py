"""
Connect method docstring: Brief description of the connect method.
"""

import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Notifications


class NotificationConsumer(WebsocketConsumer):
    """
    Class docstring: Brief description of the NotificationConsumer class.
    """

    # def connect(self):
    #     """
    #     Connect method docstring: Brief description of the connect method.
    #     """
    # async_to_sync(self.channel_layer.group_add)(
    #     "notifications", self.channel_name,
    # )
    # self.accept()
    # self.send(text_data=json.dumps(
    #     {'status': 'connected from  channel'}))
    # -------------------------------------------------------
    # self.user_id = self.scope['url_route']['kwargs']['user_id']
    # print('self.user_id', self.user_id)
    # self.room_group_name = f'user_{self.user_id}'

    # async_to_sync(self.channel_layer.group_add)(
    #     self.room_group_name,
    #     self.channel_name
    # )
    # self.accept()
    # self.send(text_data=json.dumps(
    #     {'status': 'connected to user notification channel'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self.user = None
        self.room_group_name = None

    def connect(self):
        """
        Runs upon successful connection estabalishment
        """
        self.token = self.scope['url_route']['kwargs']['token']
        print("self.token: ", self.token)
        self.user = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f"user_{self.user}"
        if self.user:
            try:
                async_to_sync(self.channel_layer.group_add)(  # type:ignore
                    self.room_group_name,
                    self.channel_name
                )
                self.accept()
            except ValueError:
                self.close()
        else:
            self.close()

    def receive(self, text_data):
        """
        Connect method docstring: Brief description of the connect method.
        """
        print(text_data)
        self.send(text_data=json.dumps({'status': 'got you'}))

    def disconnect(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def send_notification(self, event):
        """
        Connect method docstring: Brief description of the connect method.
        """
        print("channel name: ", self.channel_name)
        # if self.channel_name == event['recipient_channel']:
        # print("event: ", event)
        print("inside send_notifs in consumers.py")

        print("Received notification event:", event)
        user = event.get("user")
        message = event.get("message")
        post = event.get("post")
        print(
            f"Notification details - User: {user}, Message: {message}, Post: {post}")

        user = {
            "id": event["user"].id,
            "username": event["user"].username,
        }
        post = {
            "id": event["post"].id,
            "title": event["post"].title
        }

        message = event['message']

        post_author = event['post'].author

        print('post_author: ', post_author)
        print("message", message)
        print("post", post)

        notif = Notifications.objects.create(
            user=event["user"], message=message, post=event['post'], to=post_author)
        print("notif: ->>>>", notif)

        # print(event)

        self.send(text_data=json.dumps(
            {"message": message, 'user': user, "post": post}))
        # else:
        # print("notif ignored, not the current channel")
