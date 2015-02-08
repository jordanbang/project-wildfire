# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0003_auto_20150206_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='user',
            new_name='asker',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='type',
            new_name='question_type',
        ),
    ]
