# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0007_auto_20151113_2229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='email',
        ),
    ]
