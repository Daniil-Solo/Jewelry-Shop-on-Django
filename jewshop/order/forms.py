from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'city', 'address', 'postal_code']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'ФИО...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Электронная почта...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Номер телефона...'
            }),
            'city': forms.TextInput(attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Населенный пункт...'
            }),
            'address': forms.TextInput(attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Улица, дом, квартира...'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'item_field without_box form-control',
                'placeholder': 'Почтовый индекс...'
            }),
        }