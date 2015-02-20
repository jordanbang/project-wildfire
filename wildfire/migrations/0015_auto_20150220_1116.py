# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0014_auto_20150220_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='asker',
            field=models.ForeignKey(to='wildfire.UserProfile'),
            preserve_default=True,
        ),
    ]
