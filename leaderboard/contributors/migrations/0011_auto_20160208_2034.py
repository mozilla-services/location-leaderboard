# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_auto_20151013_2148'),
        ('contributors', '0010_auto_20160107_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='country',
            field=models.ForeignKey(default=None, to='locations.Country'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='contribution',
            name='tile',
        ),
    ]
