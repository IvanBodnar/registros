from django import forms
from django.core.exceptions import ValidationError
from .models import Hechos
from geocoder.helpers import Calle
from geocoder.exceptions import CalleNoExiste, InterseccionNoExiste


class InterseccionForm(forms.Form):

    """Crea un qs con los valores unicos para el campo 'anio'."""
    años_hechos_qs = Hechos.objects.all().distinct('anio').exclude(anio__isnull=True)

    """
    Crea una lista de tuplas para usar como choices en el form field "años".
    Filtrar a partir de que año se quiere mostrar.
    """
    años_choices = [(ho.anio, ho.anio) for ho in años_hechos_qs if ho.anio >= 2010 and ho.anio is not None]

    """Campos"""
    calle1 = forms.CharField(max_length=60,
                             label='Calle 1',
                             widget=forms.TextInput(attrs={'id': 'calle1',
                                                           'class': 'form-control',
                                                           'placeholder': 'Ingrese primera calle'}))
    calle2 = forms.CharField(max_length=60,
                             label= 'Calle 2',
                             widget=forms.TextInput(attrs={'id': 'calle2',
                                                           'class': 'form-control',
                                                           'placeholder': 'Ingrese segunda calle'}))
    radio = forms.IntegerField(min_value=10,
                               max_value=1000,
                               label='Distancia',
                               widget=forms.NumberInput(attrs={'id': 'radio',
                                                               'class': 'form-control',
                                                               'placeholder': 'En metros, Mín: 10, Máx: 1000'}))
    anios = forms.TypedMultipleChoiceField(choices=años_choices,
                                           label='Años',
                                           coerce=int,
                                           empty_value=2015,
                                           widget=forms.CheckboxSelectMultiple(attrs={'id': 'anios'}))

    """Valida si calle1 existe"""
    def clean_calle1(self):
        cleaned = self.cleaned_data['calle1'].lower()
        try:
            Calle(cleaned)
            new_calle = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])
        return new_calle

    """Valida si calle2 existe"""
    def clean_calle2(self):
        cleaned = self.cleaned_data['calle2'].lower()
        try:
            Calle(cleaned)
            new_calle = cleaned
        except CalleNoExiste as e:
            raise ValidationError(e.args[0])
        return new_calle

    """Valida si la intersección de calle1 y calle2 existe"""
    def clean(self):
        cleaned_data = super(InterseccionForm, self).clean()
        calle1 = cleaned_data.get('calle1', None)
        calle2 = cleaned_data.get('calle2', None)
        if calle1 and calle2:
            try:
                Calle(calle1) + Calle(calle2)
            except InterseccionNoExiste as e:
                raise ValidationError(e.args[0])


class TramoForm(InterseccionForm):

    altura_inicial = forms.IntegerField(min_value=0,
                                        max_value=12000,
                                        label='Altura Inicial',
                                        widget=forms.NumberInput(attrs={'id': 'altura_inicial',
                                                                        'class': 'form-control',
                                                                        'placeholder': 'Altura de inicio del tramo'}))
    altura_final = forms.IntegerField(min_value=0,
                                        max_value=12000,
                                        label='Altura Final',
                                        widget=forms.NumberInput(attrs={'id': 'altura_final',
                                                                        'class': 'form-control',
                                                                        'placeholder': 'Altura donde finaliza el tramo'}))

    def __init__(self, *args, **kwargs):
        super(TramoForm, self).__init__(*args, **kwargs)
        self.fields.pop('calle2')