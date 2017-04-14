import requests
import json


class RequestGeocoder:

    def __init__(self, url):
        self.base_url = url

    def nombre_calles(self):
        complete_url = self.base_url + 'nombres_calles/'
        return json.dumps(requests.get(complete_url, timeout=10).json())

    def interseccion(self, **kwargs):
        complete_url = self.base_url + 'interseccion/'
        respuesta = requests.get(complete_url, params=kwargs).json()
        coordenadas = respuesta['coordenadas']
        return coordenadas