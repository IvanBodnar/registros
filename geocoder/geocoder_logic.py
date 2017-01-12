from django.db import connection
from .models import CallesGeocod
from .exceptions import CalleNoExiste


def get_calles():
    """
    Returns list of street names
    :return: list
    """
    query = CallesGeocod.objects.order_by('nombre').distinct('nombre')
    return [calle.nombre for calle in query if calle.nombre is not None]


class Calle:

    def __init__(self, nombre):
        """
        Takes a street name and checks its existence
        :param nombre: str
        """
        try:
            query = "select existe_calle(%s)"
            self._ejecutar_query(query, nombre)
            self.nombre = nombre.lower()
        except:
            raise CalleNoExiste('La calle no existe')

    def _ejecutar_query(self, query, *args):
        """
        Executes the passed query
        :param query: query string properly formatted
        with %s as parameter placeholders:
        'select function(%s [...%s])'
        :param args: arguments to be passed to the query
        :return : query result. None if no result was retrieved.
        """
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            resultado = cursor.fetchone()[0]
        return resultado

    def ubicar_altura(self, altura):
        """
        Returns a string representation of the geometry
        in wgs84 crs of the point that marks
        the house number passed.
        :param altura int: house number
        :return str: string representation of geometry
        """
        query = "select st_astext(altura_direccion_calle(%s, %s))"
        return self._ejecutar_query(query, self.nombre, altura)

    def __add__(self, other):
        """
        Overloads + operator to allow the return of the geometry
        of an intersection by adding two Calle instances:
        street1 + street2
        :param other: the other Calle instance
        :return str: string representation of the point marking
        the intersection in wgs84 crs.
        """
        query = "select st_astext(punto_interseccion(%s, %s))"
        return self._ejecutar_query(query, self.nombre, other.nombre)

    def __str__(self):
        return '{}'.format(self.nombre)
