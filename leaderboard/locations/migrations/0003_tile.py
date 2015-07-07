# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20150707_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('country', models.ForeignKey(related_name='tiles', to='locations.Country')),
            ],
        ),
    ]
