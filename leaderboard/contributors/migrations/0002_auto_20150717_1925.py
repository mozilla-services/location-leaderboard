# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='observations',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together=set([('date', 'tile', 'contributor')]),
        ),
        migrations.RemoveField(
            model_name='contribution',
            name='created',
        ),
    ]
