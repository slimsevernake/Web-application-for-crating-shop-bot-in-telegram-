from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


def make_post_upload_path(instance: 'Post', filename: str) -> str:
    return f'mailings/{instance.bot.name}/{filename}'


class Post(models.Model):
    """
    Model for representing Post for mailing.
    """
    bot = models.ForeignKey(
        to="bots_management.Bot",
        on_delete=models.CASCADE,
        verbose_name="Бот",
        related_name="posts"
    )
    author = models.ForeignKey(
        to=get_user_model(),
        verbose_name="Автор",
        related_name="posts",
        on_delete=models.SET_NULL,
        default=None,
        null=True
    )
    image = models.ImageField(
        "Картинка",
        upload_to=make_post_upload_path,
        blank=True, null=True
    )
    file = models.FileField(
        "Файл",
        upload_to=make_post_upload_path,
        blank=True, null=True
    )
    url = models.URLField("Ссылка", blank=True, null=True, max_length=700)

    created_at = models.DateTimeField(
        verbose_name="Время создания",
        auto_now_add=True,
    )

    send_time = models.DateTimeField(
        verbose_name="Время отправки",
        null=True,
        blank=True
    )

    is_done = models.BooleanField(
        verbose_name="Отправка совершена?",
        default=False,
    )

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        db_table = "Posts"

    def __str__(self) -> str:
        return f"Post {self.id}"

    def get_absolute_url(self):
        return reverse(
            "bots-management:mailings:mailing-detailed",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})

    def get_update_url(self):
        return reverse(
            "bots-management:mailings:mailing-update",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})

    def get_delete_url(self):
        return reverse(
            "bots-management:mailings:mailing-delete",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})


class SentMessage(models.Model):
    """
    Model for saving chat and message info of sent Post.
    Only for Telegram messages.
    TODO:change and maybe rename model in future
    """
    chat_id = models.CharField("ID чата", max_length=255)
    message_id = models.IntegerField("ID сообщения")
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Пост, который относится к уникальному идентификатору на телеграмм сервере"
    )

    class Meta:
        verbose_name = "Уникальный идентификатор отправленного сообщения на сервере телеграмма."
        verbose_name_plural = "Уникальные идентификаторы отправленных сообщений на сервере телеграмма."
        db_table = "SentMessages"

    def __str__(self) -> str:
        return f"Sent message {self.message_id} to {self.chat_id}"
