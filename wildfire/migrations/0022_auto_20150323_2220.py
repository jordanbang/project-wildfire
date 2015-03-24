# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0021_auto_20150308_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=21),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='region',
            field=models.CharField(default=b'Toronto', max_length=20),
            preserve_default=True,
        ),
    ]
