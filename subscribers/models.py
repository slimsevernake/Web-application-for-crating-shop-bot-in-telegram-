from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from bots_management.models import Bot


class Subscriber(models.Model):
    """
    Model representing subscriber.
    """
    name = models.CharField("Ім'я", max_length=500, blank=True, null=True)
    chat_id = models.CharField("UID користувача в Telegram", max_length=24)
    info = models.TextField("Інформація про користувача", blank=True,
                            null=True, default=None)
    avatar = models.CharField(
        "Посилання на аватар", max_length=500, blank=True,
        null=True, default=None)
    is_active = models.BooleanField("В підписниках", default=True)
    created = models.DateTimeField("Створений", auto_now_add=True)
    updated = models.DateTimeField("Оновлений", auto_now=True)
    is_admin = models.BooleanField("Модератор", default=False)
    bot = models.ForeignKey(
        to=Bot, verbose_name="Яким ботом користується",
        related_name="subscribers", on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Підписники"
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
        return f"{self.name} - <{self.messengers_bot}>"

    def get_absolute_url(self) -> str:
        return reverse("subscribers:subscriber-detail",
                       kwargs={"slug": self.user_id})


class Message(models.Model):
    """
    Model representing message.
    """
    message_token = models.CharField("ID сообщения", max_length=50)
    sender = models.ForeignKey(Subscriber, on_delete=models.CASCADE,
                               related_name="messages")
    text = models.TextField("Зміст повідомлення", default=None,
                            null=True, blank=True)
    created = models.DateTimeField("Відправлено о", auto_now_add=True)
    image = models.ImageField("Картинка", upload_to="message/img",
                              blank=True, null=True)
    file = models.FileField("Файл", upload_to="message/file",
                            blank=True, null=True)
    url = models.URLField("Посилання", blank=True, null=True, max_length=700)

    class Meta:
        verbose_name = "Повідомлення"
        verbose_name_plural = "Повідомлення"
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
        if self.is_help_message:
            _, __ = HelpReply.objects.get_or_create(message=self)


class HelpReply(models.Model):
    """
    Model representing replies on help messages.
    """
    message = models.OneToOneField(
        to=Message, on_delete=models.CASCADE,
        verbose_name="Повідомлення", related_name="help_reply"
    )
    text = models.TextField("Повідомлення")
    actions = models.ManyToManyField(
        to="keyboards.Action",
        related_name="help_replies",
        verbose_name="Дії",
        blank=True,
    )
    moderator = models.ForeignKey(
        to=get_user_model(), related_name="help_replier",
        verbose_name="Модератор, що відповідає", on_delete=models.DO_NOTHING
    )

    is_started = models.BooleanField("Звернення обробляється", default=False)
    is_closed = models.BooleanField("Звернення закрито", default=False)
    created = models.DateTimeField("Створено", auto_now_add=True)
    started_at = models.DateTimeField(
        "Початок обробки зверняння", blank=True, null=True
    )
    closed_at = models.DateTimeField(
        "Кінець обробки зверняння", blank=True, null=True
    )

    class Meta:
        verbose_name = "Звернення до модератора"
        verbose_name_plural = "Звернення до модератора"

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
