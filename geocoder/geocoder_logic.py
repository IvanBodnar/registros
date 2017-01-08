from .models import CallesGeocod


def get_calles():
    """
    Returns list of street names
    :return: list
    """
    query = CallesGeocod.objects.order_by('nombre').distinct('nombre')
    return [calle.nombre for calle in query if calle.nombre is not None]
