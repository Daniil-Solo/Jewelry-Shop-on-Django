from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Пожалуйста проверьте правильность почты или пароля",
        "inactive": "К сожалению, данный аккаунт больше не активен",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Ваша почта...',
                "autofocus": True
            },
        )
        self.fields['password'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Пароль...',
                'type': 'password'
            },
        )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Почта...'
            },
        ),
        error_messages={
            'invalid': 'Пожалуйста проверьте правильность почты'
        }
    )

    error_messages = {
        "password_mismatch": "Пароли должны совпадать",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Ваше имя...',
                "autofocus": True,
            },
        )
        self.fields['password1'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Пароль...',
                'type': 'password'
            },
        )
        self.fields['password2'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Повтор пароля...',
                'type': 'password'
            },
        )
    field_order = ("username", "email", "password1", "password2")

    class Meta(UserCreationForm.Meta):
        model = User
