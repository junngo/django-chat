from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers
from chat_chat.users import models as user_models

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class Room(APIView):
    def get(self, request, format=None):
        rooms = models.Room.objects.all()
        serializer = serializers.RoomSerializer(rooms, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        # To-Do - change into serialize for creating room

        try:
            found_admin_user = user_models.User.objects.get(username='admin')

        except user_models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_contact = models.Contact.objects.create(user=user)
        new_contact.friends.add(found_admin_user)

        new_room = models.Room.objects.create()
        new_room.participants.add(new_contact)

        new_contact.save()
        new_room.save()

        return Response(status=status.HTTP_201_CREATED)
