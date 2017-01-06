from django import forms
from django.core.exceptions import ValidationError


class CallesForm(forms.Form):

    calle1 = forms.CharField(max_length=100)
    calle2 = forms.CharField(max_length=100)

    def clean_calle1(self):
        new_calle1 = (self.cleaned_data['calle1'].lower())
        if new_calle1 == 'mal':
            raise ValidationError('Dato Erroneo')

        return new_calle1