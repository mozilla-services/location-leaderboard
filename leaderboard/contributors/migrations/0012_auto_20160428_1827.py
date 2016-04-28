# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


def set_contribution_point_to_country_center(apps, schema_editor):
    Contribution = apps.get_model('contributors', 'Contribution')
    db_alias = schema_editor.connection.alias

    for contribution in Contribution.objects.using(db_alias):
        contribution.point = contribution.country.geometry.point_on_surface
        contribution.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20160208_2050'),
        ('contributors', '0011_auto_20160208_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
        ),
        migrations.RunPython(set_contribution_point_to_country_center, noop),
        migrations.RemoveField(
            model_name='contribution',
            name='country',
        ),
        migrations.AlterField(
            model_name='contribution',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
