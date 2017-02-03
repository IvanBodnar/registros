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

    def _filtrar_hechos(self):
        """
        Realiza búsqueda filtrando por años y omitiendo los siniestros con
        geometría nula.
        :return: queryset
        """
        qs = Hechos.objects\
            .filter(anio__in=self.anios)\
            .exclude(geom__isnull=True)
        return qs

    def _siniestros_radio(self):
        """
        Realiza búsqueda de los siniestros devueltos por _filtrar_hechos() que
        caen dentro del radio especificado.
        :return: queryset
        """
        qs_3857 = self._filtrar_hechos()
        siniestros_queryset = qs_3857 \
            .filter(geom_3857__distance_lt=(self.punto_3857, self.radio)) \
            .order_by('anio', 'direccion_normalizada', 'fecha')
        return siniestros_queryset

    def siniestros_queryset(self):
        """
        Filtra por los campos especificados en variable 'campos' y retorna el queryset.
        :return: queryset
        """
        qs = self._siniestros_radio()
        return qs.values(*self.campos)

    def siniestros_geojson(self):
        """
        Devuelve geojson con los campos especificados en variable 'campos'.
        :return: geojson
        """
        siniestros_qs = self._siniestros_radio()
        geojson = serialize('geojson', siniestros_qs,
                            geometry_field='geom',
                            fields=self.campos)
        return geojson