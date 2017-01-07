from django.conf.urls import url
from .views import IngresarCalles, CallesAutocomplete


urlpatterns = [
    url(r'^$', view=IngresarCalles.as_view(), name='buscador_ingresar_calle'),
    url(r'^calles-autocomplete/$', view=CallesAutocomplete.as_view(), name='calles-autocomplete')
]