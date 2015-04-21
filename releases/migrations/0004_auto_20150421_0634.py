# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('releases', '0003_auto_20150421_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='status',
            field=models.CharField(default=b'Open', max_length=1, choices=[(b'Open', b'Open'), (b'In Progress', b'In Progress'), (b'Resolved', b'Resolved'), (b'Closed', b'Closed')]),
        ),
    ]
