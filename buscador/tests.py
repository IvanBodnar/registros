from django.test import TestCase
from .siniestros import Siniestros


class PruebaTest(TestCase):
    """Carga fixture en json con algunos datos"""
    fixtures = ['data.json']

    def test_prueba(self):
        """
        Testea que devuelva el punto que esta a menos
        de 60 metros.
        """
        s = Siniestros('POINT(-58.437287 -34.586525)', 60, [2015])
        self.assertEqual(s.siniestros_radio()[0]['direccion_normalizada'], "humboldt y cabrera, jose a.")

