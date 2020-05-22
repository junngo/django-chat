from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

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
