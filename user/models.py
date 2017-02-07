import maya
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class UserStats(models.Model):

    @staticmethod
    def hora_argentina():
        return maya.now().datetime(to_timezone='America/Argentina/Buenos_Aires', naive=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True)
    fh = models.DateTimeField(default=hora_argentina)
    calle1 = models.CharField(max_length=100, null=True)
    calle2 = models.CharField(max_length=100, null=True)
    radio = models.IntegerField(null=True)
    anios = ArrayField(models.IntegerField(null=True))
    geom = models.PointField(null=True, srid=4326)



