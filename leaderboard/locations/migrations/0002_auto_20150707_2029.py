# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='iso2',
            field=models.CharField(unique=True, max_length=2, verbose_name=b'2 Digit ISO'),
        ),
        migrations.AlterField(
            model_name='country',
            name='iso3',
            field=models.CharField(unique=True, max_length=3, verbose_name=b'3 Digit ISO'),
        ),
    ]
