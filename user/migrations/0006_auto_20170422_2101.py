# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-23 00:01
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userstats_geom_tramo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstats',
            name='geom_tramo',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(null=True, srid=4326),
        ),
    ]
