# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0023_question_related_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='replyTo',
            field=models.ForeignKey(default=None, to='wildfire.Question', null=True),
            preserve_default=True,
        ),
    ]
