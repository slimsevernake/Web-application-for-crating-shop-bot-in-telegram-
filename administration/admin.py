from django.contrib import admin
from administration.models import (
    Country, DeliveryType, PaymentType, Currency
)

admin.site.register(Country)
admin.site.register(DeliveryType)
admin.site.register(PaymentType)
admin.site.register(Currency)
