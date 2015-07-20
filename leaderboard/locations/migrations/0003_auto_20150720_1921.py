# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20150715_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='mpoly',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='tile',
            old_name='mpoly',
            new_name='geometry',
        ),
    ]
