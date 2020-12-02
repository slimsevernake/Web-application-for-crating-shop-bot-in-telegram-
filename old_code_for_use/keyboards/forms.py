from django import forms

from old_code_for_use.keyboards import Button, Keyboard, Action
from old_code_for_use.keyboards import (
    get_keyboards_related_to_bot, get_buttons_related_to_keyboard,
    get_actions_related_to_bot
)


class ButtonForm(forms.ModelForm):
    action = forms.ModelChoiceField(
        queryset=None, label="Подія, яка трапиться",
        widget=forms.Select(
            attrs={'class': "form-control js-example-basic-single"}
        )
    )

    class Meta:
        model = Button
        fields = ("action", "name", "text", "description",
                   "position", "tg_row",
                  # "width", "height", "text_v_align",
                  # "text_h_align", "text_size",
                  # "bg_color",
                  # "action_type",
                  )
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            # TODO add links about using tags in text
            "text": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 3}),
            "position": forms.NumberInput(attrs={'class': 'form-control'}),
            # "width": forms.NumberInput(attrs={
            #     'class': 'form-control',
            #     'min': 1,
            #     'max': 6,
            # }),
            # "height": forms.NumberInput(attrs={
            #     'class': 'form-control',
            #     'min': 1,
            #     'max': 2,
            # }),
            "tg_row": forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 50,
            }),
            # "text_v_align": forms.Select(attrs={"class": "form-control"}),
            # "text_h_align": forms.Select(attrs={"class": "form-control"}),
            # "text_size": forms.Select(attrs={"class": "form-control"}),
            "action_type": forms.Select(attrs={"class": "form-control"}),
        #     "bg_color": forms.TextInput(attrs={"class": "form-control",
        #                                        "type": "color"}),
        }
        labels = {
            "action": "Подія, яка трапиться*",
            "name": "Назва*",
            "text": "Текст кнопки*""",
            "position": "Позиція кнопки*",
            # "width": "(V) Ширина 1-6*",
            # "height": "(V) Висота 1-2*",
            "tg_row": "(T) № рядка "
        }

    def __init__(self, *args, **kwargs):
        """
        In button form can choose only action related to current channel.
        """
        self.keyboard = kwargs.pop("keyboard", None)
        action_qs = kwargs.pop("action_qs")
        super().__init__(*args, **kwargs)

        self.fields["action"].queryset = action_qs

    def save(self, commit=True):
        """
        Automatically saves keyboard from init as parent keyboard.
        """
        button = super().save(commit=False)
        button.keyboard = self.keyboard
        if commit:
            button.save()
        return button


class ButtonAddForm(ButtonForm):
    def clean_name(self):
        """
        Checks if name is unique in this keyboard.
        """
        name = self.cleaned_data["name"]
        buttons = get_buttons_related_to_keyboard(self.keyboard)

        if name in (button.name for button in buttons):
            raise forms.ValidationError(
                "Назва кнопки має бути унікальною на одній клавіатурі"
            )

        return name

    def clean_position(self):
        """
        Checks if position is unique in this keyboard.
        """
        position = self.cleaned_data["position"]
        buttons = get_buttons_related_to_keyboard(self.keyboard)

        if position in (button.position for button in buttons):
            raise forms.ValidationError(
                "Позиція кнопки має бути унікальною на одній клавіатурі"
            )

        return position


class ButtonUpdateForm(ButtonForm):
    def clean_name(self):
        """
        If button name wasn't changed it will save.
        If was => check if it is unique in this keyboard.
        """
        name = self.cleaned_data["name"]
        buttons = get_buttons_related_to_keyboard(
            self.keyboard
        ).exclude(name=self.instance.name)

        if name in (button.name for button in buttons):
            raise forms.ValidationError(
                "Назва кнопки має бути унікальною на одній клавіатурі"
            )

        return name

    def clean_position(self):
        """
        If button position wasn't changed it will save.
        If was => check if it is unique in this keyboard.
        """
        position = self.cleaned_data["position"]
        buttons = get_buttons_related_to_keyboard(
            self.keyboard
        ).exclude(position=self.instance.position)

        if position in (button.position for button in buttons):
            raise forms.ValidationError(
                "Позиція кнопки має бути унікальною на одній клавіатурі"
            )

        return position


class KeyboardForm(forms.ModelForm):
    """"""
    name = forms.CharField(
        label="Назва клавіатури",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        required=False, label="Опис",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    # bg_color = forms.CharField(
    #     required=False, label="Колір фону клавіатури (тілько Viber)",
    #     widget=forms.TextInput(attrs={"class": "form-control",
    #                                   'type': 'color'})
    # )

    class Meta:
        model = Keyboard
        fields = ("name", "description",) #"bg_color",)

    def __init__(self, *args, **kwargs):
        self.channel = kwargs.pop("channel")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Automatically saves channel as a parent channel
        """
        keyboard = super().save(commit=False)
        keyboard.channel = self.channel
        if commit:
            keyboard.save()
        return keyboard


class KeyboardAddForm(KeyboardForm):
    def clean_name(self):
        """
        Checks if name is unique in this channel.
        """
        name = self.cleaned_data["name"]
        keyboards = get_keyboards_related_to_bot(slug=self.channel.slug)
        if name in (keyboard.name for keyboard in keyboards):
            raise forms.ValidationError("Назва має бути унікальною")

        return name


class KeyboardUpdateForm(KeyboardForm):
    def clean_name(self):
        """
        If keyboard name wasn't changed it will save.
        If was => check if it is unique.
        """
        name = self.cleaned_data["name"]
        existed_name = self.instance.name

        keyboards = get_keyboards_related_to_bot(
            slug=self.channel.slug
        ).exclude(name=existed_name)
        if name in (keyboard.name for keyboard in keyboards):
            raise forms.ValidationError("Назва має бути унікальною")

        return name


class ActionForm(forms.ModelForm):
    """
    Form to create/update action.
    Gets in init queryset of keyboards, related to channel.
    """
    action_type = forms.ChoiceField(
        choices=Action.ACTION_TYPES,
        widget=forms.Select(
            attrs={'class': "form-control js-example-basic-single"}
        )
    )
    keyboard_to_represent = forms.ModelChoiceField(
        label="Клавіатура, що відобразиться",
        queryset=None,
        widget=forms.Select(
            attrs={'class': "form-control js-example-basic-single"}
        )
    )

    class Meta:
        model = Action
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(
                attrs={"class": "form-control",
                       'rows': 3}),
            "picture": forms.FileInput(
                attrs={"class": "form-control",
                       "id": "image_preload"}),
            "video": forms.FileInput(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "sticker_id": forms.NumberInput(attrs={"class": "form-control"}),
            # "location_latitude": forms.TextInput(
            #     attrs={"class": "form-control",
            #            'required': False}
            # ),
            # "location_longitude": forms.TextInput(
            #     attrs={"class": "form-control",
            #            'required': False}
            # ),
            "description": forms.Textarea(
                attrs={"class": "form-control",
                       'rows': 3}),
            "is_info_action": forms.CheckboxInput(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        In action form can choose only keyboards related to current channel.
        """
        keyboards_qs = kwargs.pop("keyboards_qs")
        super().__init__(*args, **kwargs)

        self.fields["keyboard_to_represent"].queryset = keyboards_qs

    # def clean_location_longitude(self):
    #     lon = self.cleaned_data["location_longitude"]
    #     if lon:
    #         try:
    #             lon = float(lon)
    #         except ValueError:
    #             raise forms.ValidationError("Координати не валідні")
    #
    #         if -180 > float(lon) or float(lon) > 180:
    #             raise forms.ValidationError("Довгота від -180 до 180")
    #
    #         return lon
    #
    # def clean_location_latitude(self):
    #     lat = self.cleaned_data["location_latitude"]
    #     if lat:
    #         try:
    #             lat = float(lat)
    #         except ValueError:
    #             raise forms.ValidationError("Координати не валілні")
    #
    #         if -90 > float(lat) or float(lat) > 90:
    #             raise forms.ValidationError("Широта від -90 до 90")
    #
    #         return lat


class ActionAddForm(ActionForm):
    def clean(self):
        """
        Checks if name is unique with this keyboard.
        """
        cleaned_data = super().clean()

        name = self.cleaned_data["name"]
        keyboard_to_represent = self.cleaned_data["keyboard_to_represent"]

        actions = get_actions_related_to_bot(
            keyboard_to_represent.channel.slug
        )

        if name in (action.name for action in actions):
            self.add_error(
                "name", "Назва події з вибраною клавіатурою має бути унікальна"
            )

        return cleaned_data


class ActionUpdateForm(ActionForm):
    def clean(self):
        """
        If action's name wasn't changed it will save.
        If was => check if it is unique with chosen keyboard.
        """
        cleaned_data = super().clean()

        name = self.cleaned_data["name"]
        keyboard_to_represent = self.cleaned_data["keyboard_to_represent"]

        actions = get_actions_related_to_bot(
            keyboard_to_represent.channel.slug
        ).exclude(name=self.instance.name)

        if name in (action.name for action in actions):
            self.add_error(
                "name", "Назва події з вибраною клавіатурою має бути унікальна"
            )

        return cleaned_data
