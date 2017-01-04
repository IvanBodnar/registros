from django import forms


class CallesForm(forms.Form):

    calle1 = forms.CharField(max_length=100)
    calle2 = forms.CharField(max_length=100)