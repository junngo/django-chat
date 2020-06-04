from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers


# Create your views here.
class Home(APIView):
    def get(self, request, format=None):
        home_image = models.Home.objects.all()

        serializer = serializers.HomeImageSerializer(home_image, many=True)

        return Response(serializer.data)
