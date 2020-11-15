from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms


class ModeratorRegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'main-form__field'})
    )
    email = forms.EmailField(
        label='Поштова адреса',
        widget=forms.TextInput(attrs={'class': 'main-form__field'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True, *args, **kwargs):
        """"
            Set password to user object
        """
        obj = super().save(commit=False, *args, **kwargs)
        obj.set_password(self.cleaned_data['password'])
        if commit:
            obj.save()
        return obj


class ModeratorLoginForm(auth_forms.AuthenticationForm):
    """
    Add label and styles to default authentication form
    """
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'main-form__field',
                                      'autocomplete': "off"})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'main-form__field',
                                          'autocomplete': "off"})
    )


class ModeratorEditProfileForm(auth_forms.UserChangeForm):
    """
    Add label and styles to default UserChangeForm form
    """
    username = forms.CharField(
        label='Логін',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Ім'я",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Прізвище',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label='Поштова адреса',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password')


class ModeratorChangePasswordForm(auth_forms.PasswordChangeForm):
    """
    Add label and styles to default PasswordChangeForm form
    """
    old_password = forms.CharField(
        label='Поточний пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Підтвердження нового паролю',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
