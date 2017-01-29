from .models import Hechos
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Transform


class Siniestros:

    columnas = ['direccion_normalizada', 'fecha', 'hora', 'tipo_calle', 'anio']

    def __init__(self, punto, radio, anios):
        self.punto_3857 = self.punto_a_3857(punto)
        self.radio = radio
        self.anios = anios

    def _filtrar_hechos(self):
        qs = Hechos.objects\
            .filter(anio__in=self.anios)\
            .exclude(geom__isnull=True)
        return qs

    @staticmethod
    def punto_a_3857(punto):
        p_3857 = GEOSGeometry(punto, srid=4326)
        p_3857.transform(3857)
        return p_3857

    def siniestros_radio(self):
        qs_3857 = self._filtrar_hechos()
        resultado = qs_3857\
                    .filter(geom_3857__distance_lt=(self.punto_3857, self.radio))\
                    .order_by('anio', 'direccion_normalizada', 'fecha')
        return resultado.values(*self.columnas)

