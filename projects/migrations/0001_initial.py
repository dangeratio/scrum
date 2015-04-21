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
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('detail', models.TextField()),
                ('key_title', models.CharField(max_length=5)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'username')),
            ],
            options={
                'db_table': 'projects',
            },
        ),
    ]
