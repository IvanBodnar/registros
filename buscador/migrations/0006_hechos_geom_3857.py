# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 18:41
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0005_auto_20170124_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='hechos',
            name='geom_3857',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=3857),
        ),
    ]