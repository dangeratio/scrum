# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.FloatField()),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(default=b'o', max_length=1, choices=[(b'o', b'Open'), (b'i', b'In Progress'), (b'r', b'Resolved'), (b'c', b'Closed,')])),
                ('detail', models.TextField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('release_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'releases',
            },
        ),
    ]
