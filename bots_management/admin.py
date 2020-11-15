from django.contrib import admin
from .models import Bot


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    pass
