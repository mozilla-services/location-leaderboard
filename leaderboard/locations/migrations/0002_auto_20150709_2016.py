# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
        ),
        migrations.AlterField(
            model_name='tile',
            name='mpoly',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
        ),
    ]
