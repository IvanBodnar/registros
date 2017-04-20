import logging
import json
import requests
import datetime
#from requests.exceptions import RequestException


class RequestGeocoder:
    # Pide los datos a la api geocoder
    def __init__(self, url):
        """
        Inicializa la instancia con la url base de la
        api geocoder
        :param url str: string representando la url base de la api 
        """
        self.base_url = url
        logging.basicConfig(filename='buscador/geocoder_connection/excepciones.log', level=logging.ERROR)

    def nombre_calles(self):
        """
        Trae la lista de calles de la api geocoder
        :return: 
        """
        complete_url = self.base_url + 'nombres_calles/'
        try:
            respuesta = requests.get(complete_url, timeout=5).json()
            return json.dumps(respuesta)
        except:
            logging.exception(datetime.datetime.now())
            return None

    def interseccion(self, **kwargs):
        """
        Trae las coordenadas de la interseccion de la api geocoder
        :param kwargs: calle1 y calle2: las calles que forman la 
        interseccion
        :return: coordenadas correspondientes a la interseccion
        en formato wkt, srid 4326, ejemplo: 'POINT(-58.4756632814352 -34.6565433690812)'
        """
        complete_url = self.base_url + 'interseccion/'
        try:
            respuesta = requests.get(complete_url, params=kwargs, timeout=5)
            coordenadas = respuesta.json()['coordenadas']
            return coordenadas
        except:
            logging.exception(datetime.datetime.now())
            return None

    def tramo(self, **kwargs):

        complete_url = self.base_url + 'tramo/'
        respuesta = requests.get(complete_url, params=kwargs, timeout=5)
        respuesta_json = respuesta.json()
        coordenadas = respuesta_json['coordenadas']
        return coordenadas