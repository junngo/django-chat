from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='me', on_delete=models.CASCADE)
    friends = models.ManyToManyField(
        User, related_name='friends', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Room(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='rooms', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
