from .models import Hechos
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize


class Siniestros:

    # Campos que van a sacar siniestros_queryset() y siniestros_geojson()
    campos = ['direccion_normalizada', 'fecha', 'hora', 'tipo_calle', 'participantes', 'causa', 'anio']

    def __init__(self, punto, radio, anios):
        """
        Toma un punto alrededor del cual realiza una búsqueda de
        siniestros en el radio y años ingresados.
        :param punto: formato wkt, srid 4326, ejemplo: 'POINT(-58.4756632814352 -34.6565433690812)',
        que es el resultado de Calle('calle1') + Calle('calle2').
        :param radio: int representando el radio de búsqueda en metros.
        :param anios: list de int representando los años a buscar.
        """
        self.punto_3857 = self.punto_a_3857(punto)
        self.radio = radio
        self.anios = anios

    @staticmethod
    def punto_a_3857(punto):
        """
        Transforma el punto ingresado de srid 4236 a srid 3857 (Web Mercator).
        :param punto: punto en wkt srid 4326: 'POINT(-58.4756632814352 -34.6565433690812)'.
        :return: wkt srid 3857
        """
        p_3857 = GEOSGeometry(punto, srid=4326)
        p_3857.transform(3857)
        return p_3857

    def _filtrar_siniestros(self):
        """
        Realiza búsqueda con parámetros:
        - Filtro por años ingresados
        - Filtra siniestros con geometría nula
        - Busca los siniestros dentro del radio ingresado
        - Ordena por año, dirección y fecha
        :return: queryset
        """
        qs = Hechos.objects\
            .filter(anio__in=self.anios)\
            .exclude(geom__isnull=True) \
            .filter(geom_3857__dwithin=(self.punto_3857, self.radio)) \
            .order_by('anio', 'direccion_normalizada', 'fecha')
        return qs

    def siniestros_queryset(self):
        """
        Filtra por los campos especificados en variable 'campos' y retorna el queryset.values()
        (queryset con diccionarios como elementos en vez de objetos).
        :return: queryset.values()
        """
        qs = self._filtrar_siniestros()
        return qs.values(*self.campos)

    def siniestros_geojson(self):
        """
        Devuelve geojson con los campos especificados en variable 'campos'.
        :return: geojson
        """
        siniestros_qs = self._filtrar_siniestros()
        geojson = serialize('geojson', siniestros_qs,
                            geometry_field='geom',
                            fields=self.campos)
        return geojson