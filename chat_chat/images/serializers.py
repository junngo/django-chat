from rest_framework import serializers
from . import models

class HomeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Home
        fields = '__all__'
