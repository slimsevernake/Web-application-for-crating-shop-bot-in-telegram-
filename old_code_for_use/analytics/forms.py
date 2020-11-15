from django import forms
from django.utils import timezone

from bots_management.models import Bot


class DateInputCalendar(forms.DateInput):
    input_type = "date"


class StatisticsForm(forms.Form):
    YESTERDAY = (
        timezone.localtime(timezone.now())-timezone.timedelta(days=1)
    ).strftime('%Y-%m-%d')
    TODAY = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')

    date_from = forms.DateField(
        required=False,
        label="Від", widget=DateInputCalendar(attrs={
            "class": "form-control",
            "max": f"{TODAY}"
        })
    )
    date_to = forms.DateField(
        required=False,
        label="До", widget=DateInputCalendar(attrs={
            "class": "form-control",
            "max": f"{TODAY}"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        date_to = self.initial["get_params"].get(
            "date_to", self.TODAY
        )
        date_from = self.initial["get_params"].get(
            "date_from", self.TODAY
        )

        if date_to > date_from:
            self.fields["date_to"].initial = date_to
            self.fields["date_from"].initial = date_from
        else:
            self.fields["date_to"].initial = self.TODAY
            self.fields["date_from"].initial = self.YESTERDAY


class BotAnalyticsForm(StatisticsForm):
    ANALYTIC_CHOICES = (
        ("number", "Кількість повідомлень"),
        ("efficiency", "Ефективніть"),
    )
    MESSENGER_CHOICES = Bot.messengers
    ORDER_CHOICES = (
        ("desc", "Від найбільшого до найменьшого"),
        ("asc", "Від найменьшого до найбільшого")
    )

    analytics_type = forms.ChoiceField(
        label="Тип аналітики", choices=ANALYTIC_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    messenger = forms.ChoiceField(
        label="Мессенджер", choices=MESSENGER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    order = forms.ChoiceField(
        label="Сортування", choices=ORDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["analytics_type"].initial = self.initial["get_params"].get(
            "analytics_type", "Кількість повідомлень"
        )
        self.fields["messenger"].initial = self.initial["get_params"].get(
            "messenger", "telegram"
        )
        self.fields["order"].initial = self.initial["get_params"].get(
            "order", "Від найбільшого до найменьшого"
        )


class GeneralAnalyticsForm(StatisticsForm):
    ANALYTIC_CHOICES = (
        ("bot", "Статистика ботів"),
        ("subs", "Статистика користувачів"),
        ("subs_increase", "Приріст користувачів"),
        ("subs_decrease", "Вихід користувачів"),
    )
    analytics_type = forms.ChoiceField(
        label="Тип аналітики", choices=ANALYTIC_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["analytics_type"].initial = self.initial["get_params"].get(
            "analytics_type", "Статистика ботів"
        )
