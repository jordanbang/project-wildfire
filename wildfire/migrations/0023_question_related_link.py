# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0022_auto_20150323_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='related_link',
            field=models.URLField(max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
