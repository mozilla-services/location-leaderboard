# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20160208_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='country',
            name='lon',
        ),
        migrations.AlterField(
            model_name='country',
            name='geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]
