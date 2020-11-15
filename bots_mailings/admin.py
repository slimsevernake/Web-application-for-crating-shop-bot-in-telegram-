from django.contrib import admin

from bots_mailings.models import Post, SentMessage


@admin.register(Post)
class Post(admin.ModelAdmin):
    pass


@admin.register(SentMessage)
class Post(admin.ModelAdmin):
    pass
