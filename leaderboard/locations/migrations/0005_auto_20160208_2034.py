# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0011_auto_20160208_2034'),
        ('locations', '0004_auto_20151013_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tile',
            name='country',
        ),
        migrations.DeleteModel(
            name='Tile',
        ),
    ]
