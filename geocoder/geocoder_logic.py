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

    def ubicar_altura(self, altura):
        query = "select altura_direccion_calle(%s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, [self.nombre, altura])
            resultado = cursor.fetchone()[0]

        return resultado

    def __add__(self, other):
        query = "select punto_interseccion(%s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, [self.nombre, other.nombre])
            resultado = cursor.fetchone()[0]

        return resultado
