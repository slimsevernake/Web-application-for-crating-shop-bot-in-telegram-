from django import forms
from django.utils import timezone

from .models import HelpReply
from bots_management.models import Bot


class ReplyHelpMessageForm(forms.ModelForm):
    actions = forms.ModelMultipleChoiceField(
        queryset=None, label="Події, які надіслати",
        widget=forms.SelectMultiple(
            attrs={'class': "form-control"}
        )
    )

    class Meta:
        model = HelpReply
        fields = ("actions", "text")
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        """
        In button form can choose only action related to current channel.
        """
        action_qs = kwargs.pop("action_qs")
        super().__init__(*args, **kwargs)

        self.fields["actions"].queryset = action_qs

    def save(self, commit=True):
        reply = super().save(commit=False)

        reply.closed_at = timezone.now()
        reply.is_closed = True

        if commit:
            reply.save()

        return reply


class SubscribersChoiceForm(forms.Form):
    status = forms.ChoiceField(
        label='Статус', choices={
            ('active', 'Активні'),
            ('all', 'Всі'),
            ('not_active', 'Відписані'),
        },
        widget=forms.Select(
            attrs={'class': "form-control js-example-basic-single"}
        )
    )
