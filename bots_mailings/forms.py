from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from bots_mailings.models import Post
from bots_management.services import get_bot_by_slug
from keyboards.services import get_actions_related_to_bot
from subscribers.models import Subscriber


class MailingForm(forms.ModelForm):
    """
    Form to create a Post model object
    """
    bot = forms.Field(
        disabled=True,
        widget=forms.HiddenInput()
    )

    author = forms.Field(
        disabled=True,
        widget=forms.HiddenInput()
    )

    send_to = forms.ModelMultipleChoiceField(
        queryset=None,
        label="Відправити підписникам",
        help_text="""
            Якщо хочете відправити усім користувачам,
            залиште це поле пустим
        """,
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'class': "form-control js-example-basic-multiple",
                'multiple': "multiple"
            }
        )
    )

    actions = forms.ModelMultipleChoiceField(
        queryset=None,
        label="Контент для розсилки",
        widget=forms.SelectMultiple(
            attrs={
                'class': "form-control js-example-basic-multiple",
                'multiple': "multiple"
            }
        )
    )

    send_time = forms.DateTimeField(
        label="Час відправки",
        required=False,
        localize=True,
        help_text="Якщо хочете відправити зараз, залиште це поле пустим",
        input_formats=format("%m/%d/%y %H:%M"),
        widget=forms.DateTimeInput(
            attrs={
                'class': "form-control",
                'type': 'datetime-local'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        channel_slug = kwargs.pop('channel_slug')
        super().__init__(*args, **kwargs)
        self.fields['author'].initial = user
        self.fields['bot'].initial = get_bot_by_slug(channel_slug)
        self.fields['actions'].queryset = get_actions_related_to_bot(
            channel_slug
        )
        self.fields['send_to'].queryset = Subscriber.objects.filter(
                    bot=get_bot_by_slug(channel_slug),
                    is_active=True
                )

    def clean_send_time(self):
        """
        Checks if value of send_time field is not in the past
        :return: validated send_time
        """
        send_time = self.cleaned_data.get('send_time')
        if send_time and send_time < timezone.now():
            raise ValidationError("Розсилка не може бути виконана в минулому!")
        return send_time

    class Meta:
        fields = (
            'bot',
            'author',
            'actions',
            'send_time',
            'send_to',
        )
        model = Post


class MailingUpdateForm(MailingForm):
    """
    Form to update a Post model object
    """
    class Meta:
        model = Post
        fields = (
            'actions',
            'send_time',
            'send_to'
        )

    def clean_send_time(self):
        """
        Checks the change in time of an already sent mailing
        """
        if self.cleaned_data.get('send_time') and self.instance.is_done:
            raise ValidationError(
                "Неможливо змінити час відправки вже відпраленної розсилки!"
            )
        return super().clean_send_time()
