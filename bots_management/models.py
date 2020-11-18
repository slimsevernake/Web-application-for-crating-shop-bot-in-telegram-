from typing import Union

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Bot(models.Model):
    """
    Model for representing channel.
    Each channel has its own bots with own tokens.
    We can crete webhooks using slugs of each model.
    """
    name = models.CharField("Назва", max_length=128, unique=True)
    slug = models.SlugField("URL", max_length=128, unique=True)
    description = models.CharField(
        "Опис", max_length=250, blank=True, null=True
    )
    token = models.CharField("Токен", max_length=150, unique=True)
    owner = models.ForeignKey(
        get_user_model(), blank=True, verbose_name="Власник", on_delete=models.CASCADE
    )
    moderators = models.ManyToManyField(
        get_user_model(), blank=True, verbose_name="Модератори", related_name="bots"
    )

    is_media_allowed = models.BooleanField(
        "Дозволити обробку медія від користувача", default=True
    )

    welcome_action = models.ForeignKey(
        to="keyboards.Action", on_delete=models.DO_NOTHING,
        verbose_name="Привітальне повідомлення", blank=True,
        null=True, default=None
    )

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"
        db_table = "Bots"

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self) -> str:
        return reverse("bots-management:channel-detail",
                       kwargs={"slug": self.slug})

    def get_full_detail_url(self) -> str:
        return reverse("bots-management:channel-full-detail",
                       kwargs={"slug": self.slug})

    def get_update_url(self) -> str:
        return reverse("bots-management:channel-update",
                       kwargs={"slug": self.slug})

    def get_delete_url(self) -> str:
        return reverse("bots-management:channel-delete",
                       kwargs={"slug": self.slug})
