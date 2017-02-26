import json
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
        self.punto_4326 = GEOSGeometry(punto, srid=4326)
        self.punto_3857 = self.punto_a_3857(punto)
        self.radio = radio
        self.anios = anios

    def punto_a_3857(self, punto):
        """
        Transforma el punto ingresado de srid 4236 a srid 3857 (Web Mercator).
        :param punto: punto en wkt srid 4326: 'POINT(-58.4756632814352 -34.6565433690812)'.
        :return: wkt srid 3857
        """
        p_3857 = self.punto_4326
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
        values = qs.values(*self.campos)
        # Formatear campos
        for sin in values:
            # Evitar campos nulos
            try:
                sin['fecha'] = sin['fecha'].strftime('%d-%m-%Y')
                sin['participantes'] = ' - '.join([s for s in sin['participantes'] if s])
            except TypeError:
                pass
            sin['año'] = sin.pop('anio')
        return values

    def siniestros_geojson(self):
        """
        Devuelve un json con un geojson por cada año del queryset
        con los campos especificados en variable 'campos'.
        :return: json
        """
        resultado = dict()
        siniestros_qs = self._filtrar_siniestros()
        # Crear una lista con los años que tiene el queryset
        años = [item.anio for item in siniestros_qs.distinct('anio')]
        # Iterar sobre la lista de años, usando cada año para filtrar el
        # queryset, serializar ese filtro a geojson, agregando al dict resultado
        # un nuevo elemento compuesto por:
        # key: año, value: geojson correspondiente a ese año.
        for año in años:
            resultado[str(año)] = serialize('geojson',
                                            siniestros_qs.filter(anio=año),
                                            geometry_field='geom',
                                            fields=self.campos)
        return json.dumps(resultado)
