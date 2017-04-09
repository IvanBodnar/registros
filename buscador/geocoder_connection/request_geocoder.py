import requests


class RequestGeocoder:

    def __init__(self):
        self.base_url = 'http://104.197.96.57/'

    # def _armar_url(self, local_url):
    #     url = self.base_url + local_url
    #     return requests.get(url)


    def nombre_calles(self):
        complete_url = self.base_url + '/nombres_calles/'
        return requests.get(complete_url).json()

    def interseccion(self, **kwargs):
        complete_url = self.base_url + '/interseccion/'
        return requests.get(complete_url, params=kwargs)