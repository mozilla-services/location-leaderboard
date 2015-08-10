# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0002_auto_20150717_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='access_token',
            field=models.CharField(default='', unique=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contributor',
            name='uid',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='email',
            field=models.EmailField(default=b'', unique=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='name',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
