from django.db import models

from bots_management.models import Bot


class Category(models.Model):
    name = models.CharField("Название категории", max_length=50)
    bot = models.ForeignKey(
        Bot,
        verbose_name="Бот",
        on_delete=models.CASCADE,
        related_name="categories",
        blank=True,
    )
    description = models.TextField("Описание", max_length=255, null=True, blank=True)


class Product(models.Model):
    name = models.CharField("Название продукта", max_length=50)
    slug = models.SlugField(blank=True)
    description = models.TextField("Описание", max_length=255)
    amount = models.IntegerField("Колличество", default=0)
    article = models.CharField("Артикул", max_length=255, null=True, blank=True)
    price = models.DecimalField("Цена")
    price_with_discount = models.DecimalField("Цена со скидкой", null=True, blank=True)
    visible = models.BooleanField("Виден ли товарпользователям", default=True)
    category_id = models.ManyToManyField(
        Category,
        verbose_name="Категории",
        related_name="categories",
        blank=True
    )
    url = models.URLField(
        "Ссылка на Ваш продукт в интернет-магазине",
        blank=True,
        null=True
    )
    likes = models.IntegerField(
        "Колличество лайков",
        default=0,
        blank=True
    )
    views_count = models.IntegerField(
        "Колличество просмотров",
        default=0,
        blank=True
    )
    add_to_basket_count = models.IntegerField(
        "Колличество добавлний в корзину",
        default=0,
        blank=True
    )
    acquired_count = models.IntegerField(
        "Колличество покупок",
        default=0,
        blank=True
    )


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name="photos",
    )
    url = models.ImageField(
        "Фото товара", upload_to='add'
    )
    is_main = models.BooleanField(
        "Является ли главной", default=False
    )
