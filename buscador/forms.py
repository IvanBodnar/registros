from django import forms
from django.core.exceptions import ValidationError
from .models import Hechos
from geocoder.helpers import Calle
from geocoder.exceptions import CalleNoExiste, InterseccionNoExiste


class CallesForm(forms.Form):

    # Crea un qs con los valores unicos para el campo "anio".
    años_hechos_qs = Hechos.objects.all().distinct('anio')

    # Crea una lista de tuplas para usar como choices en el form field "años".
    # Filtrar a partir de que año se quiere mostrar.
    años_choices = [(ho.anio, ho.anio) for ho in años_hechos_qs if ho.anio >= 2010]

    calle1 = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id': 'calle1', 'class': 'form-control'}))
    calle2 = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id': 'calle2', 'class': 'form-control'}))
    radio = forms.IntegerField(min_value=10, max_value=1000,
                               widget=forms.NumberInput(attrs={'id': 'radio', 'class': 'form-control'}))
    anios = forms.TypedMultipleChoiceField(choices=años_choices, coerce=int, empty_value=2015,
                                           widget=forms.CheckboxSelectMultiple(attrs={'id': 'anios', 'class': 'check'}),
                                           label='Años')

    def clean_calle1(self):
        cleaned = self.cleaned_data['calle1'].lower()
        try:
            Calle(cleaned)
            new_calle = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])
        return new_calle

    def clean_calle2(self):
        cleaned = self.cleaned_data['calle2'].lower()
        try:
            Calle(cleaned)
            new_calle = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])
        return new_calle

    def clean(self):
        cleaned_data = super(CallesForm, self).clean()
        if cleaned_data:
            calle1 = cleaned_data['calle1'].lower()
            calle2 = cleaned_data['calle2'].lower()

            try:
                Calle(calle1) + Calle(calle2)
            except InterseccionNoExiste as e:
                raise ValidationError(e.args[0])

