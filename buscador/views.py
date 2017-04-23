import csv
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InterseccionForm, TramoForm
from .siniestros import Siniestros
from geocoder.helpers import Calle, get_calles
from user.models import UserStats
from .geocoder_connection.request_geocoder import RequestGeocoder

request_geocoder = RequestGeocoder()


def clear_session(session):
    """
    Limpia los datos de la sesion no agregados 
    por la aplicacion
    :param session: sesion a limpiar (request.session)
    :return: sesion que contiene solo las keys de django
    """
    for key in list(session.keys()):
        if key not in ['_auth_user_id', '_auth_user_backend', '_auth_user_hash']:
            del session[key]

@login_required
def ajax_calles(request):
    """
    Retorna json con los nombres de las calles para pasar
    al autocomplete de los campos calle1 y calle2
    :param request:
    :return: json
    """
    # Probar en geocoder_api, si no hay respuesta
    # caer en la app local geocoder
    calles_api = request_geocoder.nombre_calles()
    if calles_api:
        return HttpResponse(calles_api)
    else:
        return HttpResponse(json.dumps(get_calles()))


class IngresarCalles(LoginRequiredMixin, View):

    form_class = InterseccionForm
    template_name = 'buscador/forma_buscador.html'
    exito = 'buscador/tabla_buscador.html'

    def get(self, request):

        if 'calle1' and 'calle2' in request.GET:
            # Recolectar forma, usuario y sesión
            bound_form = self.form_class(request.GET)
            user = request.user
            session = request.session
            # Limpiar la sesion
            clear_session(session)

            if bound_form.is_valid():
                # Levantar los datos de la forma
                calle1 = bound_form.cleaned_data['calle1']
                calle2 = bound_form.cleaned_data['calle2']
                radio = bound_form.cleaned_data['radio']
                anios = bound_form.cleaned_data['anios']

                # Probar en geocoder_api, si no hay respuesta
                # caer en la app local geocoder
                coordenadas_api = request_geocoder.interseccion(calle1=calle1, calle2=calle2)
                if coordenadas_api:
                    coordenadas = coordenadas_api
                else:
                    coordenadas = Calle(calle1) + Calle(calle2)

                siniestros = Siniestros(coordenadas, radio, anios)

                # Cargar datos en la sesión
                session['calle1'] = calle1
                session['calle2'] = calle2
                session['radio'] = radio
                session['anios'] = anios
                session['coordenadas'] = coordenadas

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


class TramoView(LoginRequiredMixin, View):

    form_class = TramoForm
    template_name = 'buscador/forma_tramo_buscador.html'
    exito = 'buscador/tabla_buscador.html'

    def get(self, request):

        if request.GET:
            bound_form = self.form_class(request.GET)
            user = request.user
            session = request.session
            # Limpiar la sesion
            clear_session(session)

            if bound_form.is_valid():

                calle = bound_form.cleaned_data['calle']
                altura_inicial = bound_form.cleaned_data['altura_inicial']
                altura_final = bound_form.cleaned_data['altura_final']
                radio = bound_form.cleaned_data['radio']
                anios = bound_form.cleaned_data['anios']

                respuesta_api = request_geocoder.tramo(calle=calle,
                                                       inicial=altura_inicial,
                                                       final=altura_final)
                coordenadas = respuesta_api['coordenadas']

                siniestros = Siniestros(coordenadas, radio, anios)

                # Cargar datos en la sesión
                session['calle1'] = calle
                session['altura_inicial'] = altura_inicial
                session['altura_final'] = altura_final
                session['radio'] = radio
                session['anios'] = anios
                session['coordenadas'] = coordenadas

                # Instanciar y guardar estadísticas de uso
                user_stats = UserStats(user=user,
                                       session_key=session.session_key,
                                       calle1=calle,
                                       alturas_tramo=[altura_inicial, altura_final],
                                       radio=radio,
                                       anios=anios,
                                       geom_tramo=siniestros.punto_4326)
                user_stats.save()

                return render(request, self.exito, context={'items': siniestros.siniestros_queryset(),
                                                            'geojson': siniestros.siniestros_geojson()})

            else:
                return render(request=request,
                              template_name=self.template_name,
                              context={'form': bound_form})

        return render(request=request,
                      template_name=self.template_name,
                      context={'form': self.form_class()})


@login_required
def retornar_csv(request):
    calle1 = request.session.get('calle1', None)
    calle2 = request.session.get('calle2', None)
    altura_inicial = request.session.get('altura_inicial', None)
    altura_final = request.session.get('altura_final', None)
    radio = request.session.get('radio', None)
    anios = request.session.get('anios', None)
    coordenadas = request.session.get('coordenadas', None)
    delimiter = request.GET.get('radio_button', ',')

    if 'calle2' in request.session.keys():
        nombre_csv = '{}_y_{}_{}mts'.format(calle1, calle2, radio)
    else:
        nombre_csv = '{}_entre_{}_y_{}'.format(calle1, altura_inicial, altura_final)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(nombre_csv)

    siniestros = Siniestros(coordenadas, radio, anios)
    columnas = [campo.replace('anio', 'año') for campo in siniestros.campos]

    writer = csv.DictWriter(response, fieldnames=columnas, delimiter=delimiter, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for row in siniestros.siniestros_queryset():
        writer.writerow(row)

    return response
