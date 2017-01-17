from django import forms
from django.core.exceptions import ValidationError
from geocoder.helpers import Calle
from geocoder.exceptions import CalleNoExiste


class CallesForm(forms.Form):

    calle1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'calle1'}))
    calle2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'calle2'}))

    def clean_calle1(self):
        self.cleaned = self.cleaned_data['calle1'].lower()
        try:
            Calle(self.cleaned)
            new_calle1 = self.cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])

        return new_calle1

    def clean_calle2(self):
        self.cleaned = self.cleaned_data['calle2'].lower()
        try:
            Calle(self.cleaned)
            new_calle2 = self.cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])

        return new_calle2

