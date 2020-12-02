from decimal import Decimal

from django.db import models

from products.models import Product
from subscribers.models import Subscriber
from administration.models import (
    Country, DeliveryType, PaymentType
)


class MultipleActiveBasketException(Exception):
    def __init__(self, subscriber, message="Subscriber from chat {} has more than one active basket."):
        self.subscriber = subscriber
        self.message = message.format(self.subscriber.chat_id)
        super().__init__(message)

    def __str__(self):
        return self.message


class Basket(models.Model):
    subscriber = models.ForeignKey(
        Subscriber,
        verbose_name="Владелец корзины",
        on_delete=models.CASCADE,
        related_name="baskets",
    )
    is_active = models.BooleanField(default=True)
    products = models.ManyToManyField(
        Product,
        verbose_name="Товары в корзине",
        related_name="baskets",
    )
    archived = models.DateTimeField("Дата архивации", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            qs = type(self).objects.filter(subscriber=self.subscriber, is_active=True)
            if qs:
                raise MultipleActiveBasketException(self.subscriber)
        super().save(*args, **kwargs)

    @property
    def price(self) -> Decimal:
        """
        Calculate the total price of the basket
        """
        return sum(
            product.price_with_discount if product.price_with_discount else product.price
            for product in self.products.all()
        )

    def __str__(self) -> str:
        return f"Basket of {self.subscriber.chat_id} <bot: f{self.basket.subscriber.bot.name}> - (active={self.is_active})"


class Order(models.Model):
    WAITING = 'waiting'
    PROCESSING = 'processing'
    CANCELED = 'canceled'
    PAID = 'paid'
    DONE = 'done'

    STATUSES = [
        (WAITING, 'Ожидание'),
        (PROCESSING, 'В обработке'),
        (CANCELED, 'Отменён'),
        (PAID, 'Оплачен'),
        (DONE, 'Закрыт'),
    ]

    basket = models.ForeignKey(
        Basket,
        verbose_name="Корзина",
        on_delete=models.CASCADE,
        related_name="Orders",
    )
    country = models.ForeignKey(
        Country,
        verbose_name="Страна доставки",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )
    delivery_type = models.ForeignKey(
        DeliveryType,
        verbose_name="Тип доставки",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )
    payment_type = models.ForeignKey(
        PaymentType,
        verbose_name="Способ оплаты",
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.BooleanField(
        'Статус заказа',
        choices=STATUSES,
        default=WAITING,
    )

    created_stamp = models.DateTimeField("Дата создания", auto_now_add=True)
    closed_stamp = models.DateTimeField("Дата обработки", blank=True, null=True)
    city = models.CharField("Город доставки", max_length=60)

    @property
    def price(self) -> Decimal:
        """
        Return price of the order without delivery
        """
        return self.basket.price

    def __str__(self) -> str:
        return f"Order {self.basket.subscriber.chat_id} <bot: f{self.basket.subscriber.bot.name}> - {self.status}"
