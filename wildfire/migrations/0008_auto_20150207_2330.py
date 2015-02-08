# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0007_auto_20150207_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='multiple_choice_options',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceOption',
        ),
        migrations.RemoveField(
            model_name='question',
            name='range_options',
        ),
        migrations.DeleteModel(
            name='RangeOption',
        ),
        migrations.AddField(
            model_name='question',
            name='option1',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='option2',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='option3',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='option4',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='option5',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
