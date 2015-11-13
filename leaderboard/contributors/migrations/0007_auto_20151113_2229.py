# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0006_auto_20151013_2148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contributorrank',
            options={'ordering': ('rank',)},
        ),
    ]
