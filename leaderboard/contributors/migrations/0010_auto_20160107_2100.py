# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0009_auto_20151123_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='access_token',
        ),
        migrations.AddField(
            model_name='contributor',
            name='fxa_uid',
            field=models.CharField(default=None, unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
