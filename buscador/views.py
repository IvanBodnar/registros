import json
import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CallesForm
from .siniestros import Siniestros
from geocoder.helpers import Calle
from user.models import UserStats
from .geocoder_connection.request_geocoder import RequestGeocoder

request_geocoder = RequestGeocoder('http://104.197.96.57/')

@login_required
def ajax_calles(request):
    """
    Retorna json con los nombres de las calles para pasar
    al autocomplete de los campos calle1 y calle2
    :param request:
    :return: json
    """
    return HttpResponse(request_geocoder.nombre_calles())


class IngresarCalles(LoginRequiredMixin, View):

    form_class = CallesForm
    template_name = 'buscador/forma_buscador.html'
    exito = 'buscador/tabla_buscador.html'

    def get(self, request):

        if 'calle1' and 'calle2' in request.GET:
            # Recolectar forma, usuario y sesión
            bound_form = self.form_class(request.GET)
            user = request.user
            session = request.session

            if bound_form.is_valid():
                # Levantar los datos de la forma
                calle1 = bound_form.cleaned_data['calle1']
                calle2 = bound_form.cleaned_data['calle2']
                radio = bound_form.cleaned_data['radio']
                anios = bound_form.cleaned_data['anios']

                # Instanciar interseccion y siniestros
                interseccion_api = request_geocoder.interseccion(calle1=calle1, calle2=calle2)
                siniestros = Siniestros(interseccion_api, radio, anios)

                # Cargar datos en la sesión
                session['calle1'] = calle1
                session['calle2'] = calle2
                session['radio'] = radio
                session['anios'] = anios

                # Instanciar y guardar estadísticas de uso
                user_stats = UserStats(user=user,
                                       session_key=session.session_key,
                                       calle1=calle1,
                                       calle2=calle2,
                                       radio=radio,
                                       anios=anios,
                                       geom=siniestros.punto_4326)
                user_stats.save()

                return render(request, self.exito, context={'items': siniestros.siniestros_queryset(),
                                                            'geojson': siniestros.siniestros_geojson()})

            else:
                return render(request=request,
                              template_name=self.template_name,
                              context={'form': bound_form})
        else:
            return render(request=request,
                          template_name=self.template_name,
                          context={'form': self.form_class()})


@login_required
def retornar_csv(request):
    calle1 = request.session['calle1']
    calle2 = request.session['calle2']
    radio = request.session['radio']
    anios = request.session['anios']

    delimiter = request.GET.get('radio_button', ',')

    nombre_csv = '{}_y_{}_{}mts'.format(calle1, calle2, radio)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(nombre_csv)

    interseccion = Calle(calle1) + Calle(calle2)
    siniestros = Siniestros(interseccion, radio, anios)
    columnas = [campo.replace('anio', 'año') for campo in siniestros.campos]

    writer = csv.DictWriter(response, fieldnames=columnas, delimiter=delimiter)
    writer.writeheader()

    for row in siniestros.siniestros_queryset():
        writer.writerow(row)

    return response
