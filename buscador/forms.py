from django import forms
from django.core.exceptions import ValidationError
from geocoder.helpers import Calle
from geocoder.exceptions import CalleNoExiste, InterseccionNoExiste


class CallesForm(forms.Form):

    calle1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'calle1'}))
    calle2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'calle2'}))

    def clean_calle1(self):
        cleaned = self.cleaned_data['calle1'].lower()
        try:
            Calle(cleaned)
            new_calle1 = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])

        return new_calle1

    def clean_calle2(self):
        cleaned = self.cleaned_data['calle2'].lower()
        try:
            Calle(cleaned)
            new_calle2 = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])

        return new_calle2

    def clean(self):
        cleaned_data = super().clean()
        calle1 = cleaned_data['calle1']
        calle2 = cleaned_data['calle2']

        try:
            Calle(calle1) + Calle(calle2)
        except InterseccionNoExiste as e:
            raise ValidationError(e.args[0])

