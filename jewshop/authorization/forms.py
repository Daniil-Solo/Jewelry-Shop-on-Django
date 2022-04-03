from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'email_field without_box form-control',
                'placeholder': 'user@example.com'
            },
        ),
        error_messages={
            'invalid': 'Указан неверный адрес'
        }
    )
