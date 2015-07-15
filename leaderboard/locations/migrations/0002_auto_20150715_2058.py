# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tile',
            old_name='east',
            new_name='easting',
        ),
        migrations.RenameField(
            model_name='tile',
            old_name='north',
            new_name='northing',
        ),
    ]
