from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import (
    PasswordResetForm as DjangoPasswordResetForm,
    SetPasswordForm as DjangoSetPasswordForm,
    PasswordChangeForm as DjangoPasswordChangeForm
)
from django.core.exceptions import ValidationError

User = get_user_model()


class SetPasswordForm(DjangoSetPasswordForm):

    error_messages = {
        "password_mismatch": "Введенные пароли не совпадают",
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Новый пароль...',
                'type': 'password'
            },
        )
        self.fields['new_password2'].widget = forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Повтор пароля...',
                'type': 'password'
            },
        )


class PasswordChangeForm(SetPasswordForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": "Ваш старый пароль введен неверно. Пожалуйста попробуйте снова"
    }

    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.TextInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Старый пароль...',
                'type': 'password'
            }
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password


class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Ваша почта...'
            },
        ),
        error_messages={
            'invalid': 'Пожалуйста проверьте правильность почты'
        }
    )


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
