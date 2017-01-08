import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .forms import CallesForm
from geocoder.geocoder_logic import get_calles


def ajax_calles(request):
    """
    Returns json with street names to feed
    the autocomplete fields calle1 and calle2
    :param request:
    :return: json
    """
    return HttpResponse(json.dumps(get_calles()))


class IngresarCalles(View):

    form_class = CallesForm
    template_name = 'buscador/forma_buscador.html'

    def get(self, request):

        return render(request=request,
                      template_name=self.template_name,
                      context={'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            calle1 = bound_form.cleaned_data['calle1']
            calle2 = bound_form.cleaned_data['calle2']
            return HttpResponse(calle1 + calle2)
        else:
            return render(request=request,
                          template_name=self.template_name,
                          context={'form': bound_form})

