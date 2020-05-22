from django.contrib import admin
from .models import Contact, Message, Room

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
