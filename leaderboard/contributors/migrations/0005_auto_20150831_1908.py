# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20150720_1921'),
        ('contributors', '0004_auto_20150825_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributorCountryRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observations', models.IntegerField(null=True, blank=True)),
                ('rank', models.IntegerField(null=True, blank=True)),
                ('contributor', models.ForeignKey(to='contributors.Contributor')),
                ('country', models.ForeignKey(blank=True, to='locations.Country', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='contributorcountryrank',
            unique_together=set([('contributor', 'country')]),
        ),
    ]
