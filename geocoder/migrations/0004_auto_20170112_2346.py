# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 23:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geocoder', '0003_auto_20170112_2346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='callesgeocod',
            options={'managed': False},
        ),
    ]