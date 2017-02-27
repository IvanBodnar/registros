# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-27 13:04
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0006_hechos_geom_3857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acusados',
            fields=[
                ('rol', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo', models.CharField(blank=True, max_length=150, null=True)),
                ('marca', models.CharField(blank=True, max_length=50, null=True)),
                ('modelo', models.CharField(blank=True, max_length=50, null=True)),
                ('colectivo', models.CharField(blank=True, max_length=25, null=True)),
                ('interno_colectivo', models.CharField(blank=True, max_length=25, null=True)),
                ('sexo', models.CharField(blank=True, max_length=25, null=True)),
                ('edad', models.IntegerField(blank=True, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('vehiculo_numero', models.IntegerField(blank=True, null=True)),
                ('tipo_reclas_1', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'acusados',
            },
        ),
        migrations.CreateModel(
            name='Victimas',
            fields=[
                ('causa', models.CharField(blank=True, max_length=50, null=True)),
                ('rol', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo', models.CharField(blank=True, max_length=150, null=True)),
                ('marca', models.CharField(blank=True, max_length=50, null=True)),
                ('modelo', models.CharField(blank=True, max_length=50, null=True)),
                ('colectivo', models.CharField(blank=True, max_length=25, null=True)),
                ('interno_colectivo', models.CharField(blank=True, max_length=25, null=True)),
                ('sexo', models.CharField(blank=True, max_length=25, null=True)),
                ('edad', models.IntegerField(blank=True, null=True)),
                ('sumario', models.IntegerField(blank=True, null=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('tipo_recod', models.CharField(blank=True, max_length=50, null=True)),
                ('franja_edad', models.IntegerField(blank=True, null=True)),
                ('ubic_vehicm', models.CharField(blank=True, max_length=50, null=True)),
                ('franja_edad_itf', models.IntegerField(blank=True, null=True)),
                ('vehiculo_numero', models.IntegerField(blank=True, null=True)),
                ('tipo_reclas_1', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'victimas',
            },
        ),
        migrations.AddField(
            model_name='hechos',
            name='causa',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='hechos',
            name='comuna',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hechos',
            name='participantes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=None, max_length=100, null=True), default=None, size=None),
            preserve_default=False,
        ),
    ]