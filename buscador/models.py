# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


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
    comuna = models.IntegerField(blank=True, null=True)
    participantes = ArrayField(models.CharField(max_length=100, blank=True, null=True, default=None))
    geom_3857 = models.PointField(blank=True, null=True, srid=3857)
    causa = models.CharField(max_length=20, blank=True, null=True)
    tipo_colision1 = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.direccion_normalizada)

    class Meta:
        managed = True
        db_table = 'hechos'


class Acusados(models.Model):
    id_hecho = models.ForeignKey(Hechos, models.DO_NOTHING, db_column='id_hecho', blank=True, null=True)
    rol = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=150, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    colectivo = models.CharField(max_length=25, blank=True, null=True)
    interno_colectivo = models.CharField(max_length=25, blank=True, null=True)
    sexo = models.CharField(max_length=25, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    vehiculo_numero = models.IntegerField(blank=True, null=True)
    tipo_reclas_1 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.sexo, self.edad)

    class Meta:
        managed = True
        db_table = 'acusados'


class Victimas(models.Model):
    id_hecho = models.ForeignKey(Hechos, models.DO_NOTHING, db_column='id_hecho', blank=True, null=True)
    causa = models.CharField(max_length=50, blank=True, null=True)
    rol = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=150, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    colectivo = models.CharField(max_length=25, blank=True, null=True)
    interno_colectivo = models.CharField(max_length=25, blank=True, null=True)
    sexo = models.CharField(max_length=25, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    sumario = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    tipo_recod = models.CharField(max_length=50, blank=True, null=True)
    franja_edad = models.IntegerField(blank=True, null=True)
    ubic_vehicm = models.CharField(max_length=50, blank=True, null=True)
    franja_edad_itf = models.IntegerField(blank=True, null=True)
    vehiculo_numero = models.IntegerField(blank=True, null=True)
    tipo_reclas_1 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '{}, {}'.format(self.sexo, self.edad)

    class Meta:
        managed = True
        db_table = 'victimas'
