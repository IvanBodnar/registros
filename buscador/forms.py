from django import forms
from django.core.exceptions import ValidationError
from dal import autocomplete
from geocoder.models import CallesGeocod


class CallesForm(forms.Form):
    queryset_calles = CallesGeocod.objects.all().order_by('nombre').distinct('nombre')
    widget_autocomplete = autocomplete.ModelSelect2(url='calles-autocomplete',
                                                    attrs={'data-placeholder': 'Ingrese Calle',
                                                           'data-minimum-input-length': 3,
                                                           })

    calle1 = forms.ModelChoiceField(
        queryset=queryset_calles,
        widget=widget_autocomplete
    )
    calle2 = forms.ModelChoiceField(
        queryset=queryset_calles,
        widget=widget_autocomplete
    )

    def clean_calle1(self):
        new_calle1 = (self.cleaned_data['calle1'].lower())
        if new_calle1 == 'mal':
            raise ValidationError('Dato Erroneo')

        return new_calle1
