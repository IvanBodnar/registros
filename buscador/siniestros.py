from .models import Hechos
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db.models.functions import Transform


class Siniestros:

    def __init__(self, punto, radio, anios):
        self.punto = self.punto_a_3857(punto)
        self.radio = radio
        self.anios = anios

    def _filtrar_hechos(self):
        qs = Hechos.objects\
            .filter(anio__in=self.anios)\
            .exclude(geom__isnull=True)\
            .annotate(transform=Transform('geom', srid=3857))\
            .all()
        for q in qs:
            q.geom = q.transform
        return qs

    @staticmethod
    def punto_a_3857(punto):
        ge = GEOSGeometry(punto, srid=4326)
        ge.transform(3857)
        return ge

