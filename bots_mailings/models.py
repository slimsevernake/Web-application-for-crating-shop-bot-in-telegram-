from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


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

    created_at = models.DateTimeField(
        verbose_name="Час створення",
        auto_now_add=True,
    )

    actions = models.ManyToManyField(
        to="keyboards.Action",
        verbose_name="Дії",
        related_name="posts",
    )

    send_time = models.DateTimeField(
        verbose_name="Час відправки",
        null=True,
        blank=True
    )

    is_done = models.BooleanField(
        verbose_name="Відправлення здійснене?",
        default=False,
    )

    class Meta:
        verbose_name = "Публікація"
        verbose_name_plural = "Публікації"
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
    chat_id = models.CharField("ID чату", max_length=255)
    message_id = models.IntegerField("ID повідомлення")
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Пост, який відноситься до відправленного повідомлення"
    )
    # TODO: still think about this possibility
    # TODO: it will be used in updating messages
    # action = models.ForeignKey(
    #     to="keyboards.Action",
    #     on_delete=models.CASCADE,
    #     verbose_name="Дія, яка відноситься до відправленного повідомлення",
    #     related_name="sent_posts"
    # )

    class Meta:
        verbose_name = "Повідомлення відправленої публікації"
        verbose_name_plural = "Повідомлення відправленої публікації"
        db_table = "SentMessages"


    def __str__(self) -> str:
        return f"Sent message {self.message_id} to {self.chat_id}"
