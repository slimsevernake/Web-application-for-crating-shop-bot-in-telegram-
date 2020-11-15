from django.contrib import admin

from subscribers.models import Subscriber, Message, HelpReply


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "is_admin")
    list_filter = ("is_active", "is_admin")
    search_fields = ("name", "info")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "created")


@admin.register(HelpReply)
class HelpReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "text", "is_started", "is_closed")
    list_filter = ("is_started",)
