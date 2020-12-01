from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from bots_management.models import Bot


class BotForm(forms.ModelForm):
    name = forms.CharField(
        label='Название бота',
        widget=forms.TextInput(attrs={'class': 'form-control modal__field',
                                      'id': 'i_title'}),
        help_text="*Название бота лишь для отображения на сайте",
        error_messages={'unique': 'Бот с таким названием уже существет'}
    )
    token = forms.CharField(
        label='Телеграм токен',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="*Токен должен быть уникальным для каждого бота",
        error_messages={'unique': 'Бот с таким токеном уже существет'}
    )

    description = forms.CharField(
        label='Описание',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control modal__field',
            'id': 'i_description'
        }),
        help_text="*Описание бота лишь для отображения на сайте"
    )

    moderators = forms.ModelMultipleChoiceField(
        label='Модераторы',
        # help_text="Если не хотите добавлять модератов, то оставьте это поле пустым.",
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'class': "form-control js-example-basic-multiple select2-search",
                'id': "i_moderators",
                'multiple': "multiple"
            }
        )
    )

    class Meta:
        model = Bot
        fields = (
            'name',
            'token',
            'description',
            'moderators',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Automatically saves user, who's created a channel as a moder, and try to set webhook
        """
        bot = super().save(commit=False)
        bot.slug = slugify(self.cleaned_data["name"])
        if not bot.owner:
            bot.owner = self.user
        if commit:
            bot.save()
        return bot

