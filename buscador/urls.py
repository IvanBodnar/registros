from django.conf.urls import url
from .views import IngresarCalles, ajax_calles, retornar_csv


urlpatterns = [
    url(r'^$', view=IngresarCalles.as_view(), name='buscador_ingresar_calle'),
    url(r'^calles', ajax_calles, name='ajax_calles'),
    url(r'^csv', retornar_csv, name='retornar_csv'),
]