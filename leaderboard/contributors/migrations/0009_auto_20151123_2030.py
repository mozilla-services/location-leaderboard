# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0008_remove_contributor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='name',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
