# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0016_auto_20150220_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatarUrl',
            field=models.URLField(max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
