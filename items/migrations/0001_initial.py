# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('detail', models.TextField()),
                ('type', models.CharField(default=b'b', max_length=1, choices=[(b'b', b'Bug'), (b'i', b'Improvement'), (b'f', b'Feature'), (b't', b'Task')])),
                ('priority', models.IntegerField(default=3, choices=[(1, b'Low'), (2, b'Low-Med'), (3, b'Medium'), (4, b'Medium-High'), (5, b'High')])),
                ('effort', models.IntegerField(default=3, choices=[(1, b'Hour'), (2, b'Hours'), (3, b'Day'), (4, b'Days'), (5, b'Week'), (6, b'Weeks')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_started', models.DateTimeField()),
                ('date_completed', models.DateTimeField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'username')),
            ],
            options={
                'db_table': 'items',
            },
        ),
    ]
