import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .forms import CallesForm
from geocoder.helpers import get_calles, Calle
from .siniestros import Siniestros


def ajax_calles(request):
    """
    Retorna json con los nombres de las calles para pasar
    al autocomplete de los campos calle1 y calle2
    :param request:
    :return: json
    """
    return HttpResponse(json.dumps(get_calles()))


class IngresarCalles(View):

    form_class = CallesForm
    template_name = 'buscador/forma_buscador.html'
    exito = 'buscador/tabla_buscador.html'

    def get(self, request):
        if 'calle1' and 'calle2' in request.GET:
            bound_form = self.form_class(request.GET)

            if bound_form.is_valid():
                calle1 = bound_form.cleaned_data['calle1']
                calle2 = bound_form.cleaned_data['calle2']
                interseccion = Calle(calle1) + Calle(calle2)
                siniestros = Siniestros(interseccion, 1000, [2013, 1014, 2015])

                return render(request, self.exito, context={'items': siniestros.siniestros_radio()})

            else:
                return render(request=request,
                              template_name=self.template_name,
                              context={'form': bound_form})
        else:
            return render(request=request,
                          template_name=self.template_name,
                          context={'form': self.form_class()})



