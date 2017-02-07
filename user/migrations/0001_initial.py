# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-07 15:10
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.contrib.gis.db import models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40, null=True)),
                ('fh', models.DateTimeField(auto_now=True)),
                ('calle1', models.CharField(max_length=100, null=True)),
                ('calle2', models.CharField(max_length=100, null=True)),
                ('radio', models.IntegerField(null=True)),
                ('anios', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=None)),
                ('geom', django.contrib.gis.db.models.PointField(null=True, srid=4326)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
