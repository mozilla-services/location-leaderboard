# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0005_auto_20150902_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributorrank',
            name='contributor',
            field=models.ForeignKey(related_name='ranks', to='contributors.Contributor'),
        ),
    ]
