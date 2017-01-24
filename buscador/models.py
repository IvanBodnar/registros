# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models


class Hechos(models.Model):
    orden = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    mes = models.IntegerField(blank=True, null=True)
    comisaria = models.CharField(max_length=5, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    tipo_colision = models.CharField(max_length=100, blank=True, null=True)
    lugar_hecho = models.CharField(max_length=200, blank=True, null=True)
    direccion_normalizada = models.CharField(max_length=200, blank=True, null=True)
    tipo_calle = models.CharField(max_length=50, blank=True, null=True)
    direccion_normalizada_arcgis = models.CharField(max_length=200, blank=True, null=True)
    calle1 = models.CharField(max_length=100, blank=True, null=True)
    altura = models.IntegerField(blank=True, null=True)
    calle2 = models.CharField(max_length=100, blank=True, null=True)
    codigo_calle = models.IntegerField(blank=True, null=True)
    codigo_cruce = models.IntegerField(blank=True, null=True)
    geocodificacion = models.CharField(max_length=300, blank=True, null=True)
    franja_horaria = models.IntegerField(blank=True, null=True)
    dia_semana = models.IntegerField(blank=True, null=True)
    semestre = models.IntegerField(blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True, srid=4326)
    cantidad_victimas = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    fh = models.DateTimeField(blank=True, null=True)
    geom_3857 = models.PointField(blank=True, null=True, srid=3857)

    class Meta:
        managed = True
        db_table = 'hechos'
