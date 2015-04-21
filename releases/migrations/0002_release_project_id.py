# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('releases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='project_id',
            field=models.ForeignKey(db_column=b'projects.title', default=b'', to='projects.Project'),
        ),
    ]
