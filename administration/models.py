from django.db import models


class Country(models.Model):
    """
    All available countries for our project
    """
    name = models.CharField("Название страны для доставки", max_length=60, unique=True)
    iso2 = models.CharField("Код страны", max_length=2, unique=True)
    slug = models.SlugField("Slug")

    def __str__(self) -> str:
        return self.name.title()


class DeliveryType(models.Model):
    """
    All available delivery type for our project
    """
    name = models.CharField("Название типа доставки", max_length=60)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="deliveries",
        verbose_name="Страна службы доставки",
        blank=True,
        null=True
    )
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self) -> str:
        return f"{self.name.title()} - {self.country.name.title()}"


class PaymentType(models.Model):
    """
    All available delivery type for our project
    """
    name = models.CharField("Название типа доставки", max_length=60)
    slug = models.SlugField("Slug")

    def __str__(self) -> str:
        return self.name.title()


class Currency(models.Model):
    """
    All available currencies for our project
    """
    name = models.CharField("Название валюты", max_length=60)
    symbol = models.CharField("Символ", max_length=1)
    country_id = models.OneToOneField(
        Country,
        verbose_name="Валюта страны",
        related_name="currency",
        on_delete=models.CASCADE,
    )
