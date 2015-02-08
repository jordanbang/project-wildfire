# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0006_auto_20150207_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(max_length=2, choices=[(b'MC', b'Multiple Choice'), (b'RG', b'Range'), (b'TF', b'True or False'), (b'RA', b'Rating')]),
            preserve_default=True,
        ),
    ]
