from django.contrib import admin

from .models import Action, Keyboard, Button


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("get_channel", "name", "keyboard_to_represent")

    def get_channel(self, obj):
        return obj.keyboard_to_represent.channel

    get_channel.short_description = "Канал"


@admin.register(Keyboard)
class KeyboardAdmin(admin.ModelAdmin):
    list_display = ("bot", "name")


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ("get_channel", "keyboard", "action", "name",
                    "position",)

    def get_channel(self, obj):
        return obj.keyboard.channel

    get_channel.short_description = "Канал"
