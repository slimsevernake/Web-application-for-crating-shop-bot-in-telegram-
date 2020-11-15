from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from bots_management.models import Bot
from bots_management.services import get_all_bots
from keyboards.models import Action


class BotForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва боту',
        widget=forms.TextInput(attrs={'class': 'form-control modal__field',
                                      'id': 'i_title'})
    )
    slug = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control modal__field',
                                      'id': 'i_url'})
    )
    token = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    is_media_allowed = forms.CheckboxInput(attrs={
        'class': 'form-control modal__field',
        'id': 'i_allowUserMedia'
    })
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control modal__field',
            'id': 'i_description'
        })
    )
    welcome_action = forms.ModelChoiceField(
        label='Привітальне повідомлення', required=False,
        queryset=Action.objects.none(),
        widget=forms.Select(
            attrs={'class': "form-control js-example-basic-single"}
        )
    )
    moderators = forms.ModelMultipleChoiceField(
        label='Модератори', queryset=get_user_model().objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': "select2-search",
                   'id': "i_moderators"}
        )
    )

    class Meta:
        model = Bot
        fields = (
            'name',
            'slug',
            'token',
            'description',
            'moderators',
            'is_media_allowed',
            'welcome_action'
        )

    def clean_token(self):
        token = self.cleaned_data.get("token")
        bots = get_all_bots()

        if token in (bot.token for bot in bots):
            raise ValidationError("Такий токен вже існує")

        return token


class BotUpdateForm(BotForm):
    class Meta:
        model = Bot
        fields = ("token", "description",)
        widgets = {
            "token": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'})
        }
