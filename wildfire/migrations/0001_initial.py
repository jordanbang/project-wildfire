# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice1', models.CharField(max_length=40)),
                ('choice2', models.CharField(max_length=40)),
                ('choice3', models.CharField(max_length=40)),
                ('choice4', models.CharField(max_length=40)),
                ('choice5', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=20)),
                ('date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RangeOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lower_bound', models.IntegerField(default=0)),
                ('upper_bound', models.IntegerField(default=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('region', models.CharField(max_length=20)),
                ('join_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(to='wildfire.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='question',
            field=models.ManyToManyField(to='wildfire.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='wildfire.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(to='wildfire.User'),
            preserve_default=True,
        ),
    ]
