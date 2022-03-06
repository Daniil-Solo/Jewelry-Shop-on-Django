from django import forms


class CartAddJewelryForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=(None, ), label="Количество", coerce=int,
                                      widget=forms.Select(attrs={'id': 'quantity_select', 'class': "form-select"}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def set_choices(self, max_quantity=1):
        choice_list = list(range(1, max_quantity + 1))
        self.fields['quantity'].choices = [(i, str(i)) for i in choice_list]
        return self
