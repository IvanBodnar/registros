from django import forms
from django.core.exceptions import ValidationError
from geocoder.helpers import Calle
from geocoder.exceptions import CalleNoExiste, InterseccionNoExiste


class CallesForm(forms.Form):

    calle1 = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id': 'calle1'}))
    calle2 = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id': 'calle2'}))

    def _calles_cleaner(self, cleaned):
        try:
            Calle(cleaned)
            new_calle = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])
        return new_calle

    def clean_calle1(self):
        cleaned = self.cleaned_data['calle1'].lower()
        self._calles_cleaner(cleaned=cleaned)

    def clean_calle2(self):
        cleaned = self.cleaned_data['calle2'].lower()
        self._calles_cleaner(cleaned=cleaned)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            calle1 = cleaned_data['calle1'].lower()
            calle2 = cleaned_data['calle2'].lower()

            try:
                Calle(calle1) + Calle(calle2)
            except InterseccionNoExiste as e:
                raise ValidationError(e.args[0])

