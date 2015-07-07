# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_tile'),
        ('contributors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('observations', models.PositiveIntegerField()),
                ('contributor', models.ForeignKey(to='contributors.Contributor')),
                ('tile', models.ForeignKey(to='locations.Tile')),
            ],
        ),
    ]
