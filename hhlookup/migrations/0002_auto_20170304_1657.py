# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-04 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhlookup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='flags',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
