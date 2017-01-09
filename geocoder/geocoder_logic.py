from django.db import connection
from .models import CallesGeocod


def get_calles():
    """
    Returns list of street names
    :return: list
    """
    query = CallesGeocod.objects.order_by('nombre').distinct('nombre')
    return [calle.nombre for calle in query if calle.nombre is not None]


class Calle:

    def __init__(self, nombre):
        self.nombre = nombre

    def _ejecutar_query(self, query, *args):
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            resultado = cursor.fetchone()[0]
        return resultado

    def ubicar_altura(self, altura):
        query = "select altura_direccion_calle(%s, %s)"
        return self._ejecutar_query(query, self.nombre, altura)

    def __add__(self, other):
        query = "select punto_interseccion(%s, %s)"
        return self._ejecutar_query(query, self.nombre, other.nombre)
