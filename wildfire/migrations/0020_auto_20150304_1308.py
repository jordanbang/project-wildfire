# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildfire', '0019_auto_20150301_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connected',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user1', models.ForeignKey(related_name='connected_1', to='wildfire.UserProfile')),
                ('user2', models.ForeignKey(related_name='connected_2', to='wildfire.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='connected',
            unique_together=set([('user1', 'user2')]),
        ),
    ]
