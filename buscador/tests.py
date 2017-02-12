from django.test import TestCase
from .siniestros import Siniestros


class SiniestrosTest(TestCase):

    s = Siniestros('POINT (-58.44701261 -34.62288732)', 10, [2015])
    fixtures = ['data1.json']

    def test_transforma_punto_de_4326_a_3857(self):
        self.assertEqual(str(self.s.punto_a_3857()), 'SRID=3857;POINT (-6506291.682133242 -4112750.400425036)')

    def test_siniestros_queryset(self):
        self.assertEqual(self.s.siniestros_queryset()[0]['direccion_normalizada'], "rivadavia av. y paysandu")