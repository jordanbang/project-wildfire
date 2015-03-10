# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0020_auto_20150304_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetedQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.ForeignKey(to='wildfire.Question')),
                ('user', models.ForeignKey(to='wildfire.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='targetedquestion',
            unique_together=set([('user', 'question')]),
        ),
    ]
