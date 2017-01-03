from django.conf.urls import url
from .views import IngresarCalles


urlpatterns = [
    url(r'^$', view=IngresarCalles.as_view(), name='buscador_ingresar_calle')
]