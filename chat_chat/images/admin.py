from django.contrib import admin
from .models import Home

# Register your models here.
@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    pass
