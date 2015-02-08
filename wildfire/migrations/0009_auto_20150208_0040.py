# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0008_auto_20150207_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='question',
            field=models.ManyToManyField(related_name='categories', to='wildfire.Question'),
            preserve_default=True,
        ),
    ]
