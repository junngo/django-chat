import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import models
from .exceptions import ClientError
from .utils import get_room_or_error

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name
        # self.user = self.scope["user"]

        # # Join room group
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        # await self.accept()
        # if self.scope["user"].is_anonymous:
        #     # Reject the connection
        #     await self.close()
        # else:
        #     # Accept the connection
        await self.accept()
        # Store which rooms the user has joined on this connection
        self.rooms = set()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except ClientError:
                pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = json.loads(text_data)

        # Messages will have a "command" key we can switch on
        command = message.get("command", None)
        try:
            if command == "join":
                # Make them join the room
                await self.join_room(message["room"])
            elif command == "leave":
                # Leave the room
                await self.leave_room(message["room"])
            elif command == "send":
                await self.send_room(message["room"], message["message"])

        except ClientError as e:
            # Catch any errors and send it back
            await self.send(text_data=json.dumps({
                "error": e.code
            }))


    ##### Command helper methods called by receive_json

    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])

        # Send a join message if it's turned on
        # if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        if True:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat_join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )

        # Store that we're in the room
        self.rooms.add(room_id)

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )

        # Instruct their client to finish opening the room
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "join": str(room.id),
            "title": str(room.id),  # Do we need room title?
        }))


    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])

        # Send a leave message if it's turned on
        # if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        if True:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat_leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )

        # Remove that we're in the room
        self.rooms.discard(room_id)

        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )

        # Instruct their client to finish closing the room
        await self.send(text_data=json.dumps({
            "leave": str(room.id),
        }))

    async def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")

        # Get the room and send to the group about it
        room = await get_room_or_error(room_id, self.scope["user"])

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat_message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )


    ##### Handlers for messages sent over the channel layer

    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send(text_data=json.dumps({
                "msg_type": "4",
                "room": event["room_id"],
                "username": event["username"],
        }))

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send(text_data=json.dumps({
                "msg_type": "5",
                "room": event["room_id"],
                "username": event["username"],
        }))

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send(text_data=json.dumps({
                "msg_type": "0",
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
        }))
