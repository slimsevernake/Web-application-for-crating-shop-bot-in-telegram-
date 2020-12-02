from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from bots_mailings.models import Post
from bots_management.services import get_bot_by_slug
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
            Если хотеите отправить всем подписчикам оставьте это поле пустым 
        """,
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'class': "form-control js-example-basic-multiple",
                'multiple': "multiple"
            }
        )
    )

    #TODO:add fields

    send_time = forms.DateTimeField(
        label="Час відправки",
        required=False,
        localize=True,
        help_text="Если хотите отправить сейчас - оставьте это поле пустым",
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
        self.fields['actions'].queryset = None,
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
            raise ValidationError("Невозможно отправить сообщение в прошлом!")
        return send_time

    class Meta:
        fields = (
            'bot',
            'author',
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
            'send_time',
            'send_to'
        )

    def clean_send_time(self):
        """
        Checks the change in time of an already sent mailing
        """
        if self.cleaned_data.get('send_time') and self.instance.is_done:
            raise ValidationError(
                "Невозможно изменить время отправки уже отправленного сообщения"
            )
        return super().clean_send_time()
