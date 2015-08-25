# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0003_auto_20150810_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='name',
            field=models.CharField(default=b'', unique=True, max_length=255),
        ),
    ]
