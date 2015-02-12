# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0009_auto_20150208_0040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_type',
            new_name='questionType',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='join_date',
            new_name='joinDate',
        ),
        migrations.AddField(
            model_name='user',
            name='avatarUrl',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
