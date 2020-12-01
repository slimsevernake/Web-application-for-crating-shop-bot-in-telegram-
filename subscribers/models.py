from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from bots_management.models import Bot


def make_message_upload_path(instance: 'Message', filename: str) -> str:
    return f'messages/{instance.sender.bot.name}/{filename}'


def make_reply_upload_path(instance: 'Reply', filename: str) -> str:
    return f'messages/{instance.message.sender.bot.name}/{filename}'


class Subscriber(models.Model):
    """
    Model representing subscriber.
    """
    name = models.CharField("Имя", max_length=500, blank=True, null=True)
    chat_id = models.CharField("UID чата в Telegram", max_length=24)
    info = models.TextField("Информация о пользвателе", blank=True,
                            null=True, default=None)
    avatar = models.CharField(
        "Ссылка на аватар", max_length=500, blank=True,
        null=True, default=None)
    is_active = models.BooleanField("Находится ли он в подписчиках", default=True)
    created = models.DateTimeField("Созданный", auto_now_add=True)
    updated = models.DateTimeField("Обновлен", auto_now=True)
    is_admin = models.BooleanField("Модератор", default=False)
    bot = models.ForeignKey(
        to=Bot, verbose_name="Каким ботом пользуется",
        related_name="subscribers", on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        db_table = "Subscribers"
        unique_together = [["chat_id", "bot"]]

    def ban_user(self):
        """
        Ban current user.
        """
        if self.is_active is True:
            self.is_active = False
            self.save()

    def __str__(self) -> str:
        return f"{self.name} - <{self.bot}>"

    def get_absolute_url(self) -> str:
        return reverse("subscribers:subscriber-detail",
                       kwargs={"slug": self.chat_id})


class Message(models.Model):
    """
    Model representing message.
    """
    message_token = models.CharField("ID сообщения", max_length=50)
    sender = models.ForeignKey(Subscriber, on_delete=models.CASCADE,
                               related_name="messages")
    text = models.TextField("Содержание сообщения", default=None,
                            null=True, blank=True)
    created = models.DateTimeField("Отправлено в ", auto_now_add=True)
    image = models.ImageField(
        "Изображение",
        upload_to=make_message_upload_path,
        blank=True, null=True
    )
    file = models.FileField(
        "Файл",
        upload_to=make_message_upload_path,
        blank=True, null=True
    )
    url = models.URLField("Ссылка", blank=True, null=True, max_length=700)

    class Meta:
        verbose_name = "Сообщения пользователей"
        verbose_name_plural = "Сообщение"
        db_table = "Messages"

    def __str__(self) -> str:
        return f"{self.text}"

    def delete(self, *args, **kwargs):
        """
        deletes files if message is deleted.
        """
        if self.file:
            self.file.delete()
        if self.image:
            self.image.delete()

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # _, __ = HelpReply.objects.get_or_create(message=self)


class Reply(models.Model):
    """
    Model representing replies on help messages.
    """
    message = models.OneToOneField(
        to=Message, on_delete=models.CASCADE,
        verbose_name="Сообщение", related_name="help_reply"
    )
    text = models.TextField("Текст ответа")
    image = models.ImageField(
        "Изображения для ответа",
        upload_to=make_reply_upload_path,
        blank=True, null=True
    )
    file = models.FileField(
        "Файл для ответа",
        upload_to=make_reply_upload_path,
        blank=True, null=True
    )
    url = models.URLField("Ссылка для ответа", blank=True, null=True, max_length=700)
    moderator = models.ForeignKey(
        to=get_user_model(), related_name="help_replier",
        verbose_name="Модератор, который взаимодействует", on_delete=models.DO_NOTHING
    )

    is_started = models.BooleanField("Соощения пользователя в обработке", default=False)
    is_closed = models.BooleanField("Сообщения пользователя обработано", default=False)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    started_at = models.DateTimeField(
        "Начало обработки:", blank=True, null=True
    )
    closed_at = models.DateTimeField(
        "Конец обработки:", blank=True, null=True
    )

    class Meta:
        verbose_name = "Ответ модератора"
        verbose_name_plural = "Ответы модераторов"

    def __str__(self) -> str:
        if self.is_closed:
            return f"CLOSED {self.message.sender.name}"
        return f"OPEN {self.message.sender.name}"

    def get_absolute_url(self):
        return reverse(
            "bots-management:subscribers:help-message-detail",
            kwargs={"slug": self.message.sender.bot.slug,
                    "pk": self.pk}
        )

    def get_reply_url(self):
        return reverse(
            "bots-management:subscribers:help-message-reply",
            kwargs={"slug": self.message.sender.bot.slug,
                    "pk": self.pk}
        )
