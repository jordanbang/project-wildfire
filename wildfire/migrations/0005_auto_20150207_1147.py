# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0004_auto_20150206_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='join_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
