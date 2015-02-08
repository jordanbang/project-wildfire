# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0005_auto_20150207_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='multiple_choice_options',
            field=models.ForeignKey(default=None, blank=True, to='wildfire.MultipleChoiceOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='range_options',
            field=models.ForeignKey(default=None, blank=True, to='wildfire.RangeOption', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
