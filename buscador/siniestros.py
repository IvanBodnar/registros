from .models import Hechos
from django.contrib.gis.geos import GEOSGeometry, Point


class Siniestros:

    def __init__(self, punto, radio, anios):
        self.punto = punto
        self.radio = radio
        self.anios = anios

    def _filtrar_anios(self):
        return Hechos.objects.filter(anio__in=self.anios)

    def punto_a_3857(self, punto):
        ge = GEOSGeometry(punto, srid=4326)
        ge.transform(3857)
        return ge.x, ge.y

