# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0002_release_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='detail',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='release',
            name='number',
            field=models.FloatField(default=b''),
        ),
        migrations.AlterField(
            model_name='release',
            name='project_id',
            field=models.ForeignKey(to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='release',
            name='release_date',
            field=models.DateTimeField(default=b''),
        ),
        migrations.AlterField(
            model_name='release',
            name='status',
            field=models.CharField(default=b'o', max_length=1, choices=[(b'o', b'Open'), (b'i', b'In Progress'), (b'r', b'Resolved'), (b'c', b'Closed')]),
        ),
    ]
