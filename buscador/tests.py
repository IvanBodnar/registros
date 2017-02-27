from django.test import TestCase
from django.urls import reverse
from .siniestros import Siniestros
from django.http import HttpRequest
from .views import IngresarCalles



class SiniestrosTest(TestCase):

    s = Siniestros('POINT (-58.44701261 -34.62288732)', 10, [2015])
    fixtures = ['data1.json']

    def test_transforma_punto_de_4326_a_3857(self):
        self.assertEqual(str(self.s.punto_a_3857()), 'SRID=3857;POINT (-6506291.682133242 -4112750.400425036)')

    def test_siniestros_queryset(self):
        self.assertEqual(self.s.siniestros_queryset()[0]['direccion_normalizada'], "rivadavia av. y paysandu")

    def test_siniestros_geojson(self):
        self.assertTrue(isinstance(self.s.siniestros_geojson(), str))
        self.assertEqual(len(self.s.siniestros_geojson()), 503)


class IngresarCalleViewsTestCase(TestCase):

    def test_forma_buscador(self):
        request = HttpRequest()
        response = IngresarCalles().get(request)
        self.assertIn(b'Buscador', response.content)