# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhlookup', '0002_auto_20170304_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='old_index',
            field=models.IntegerField(default=-1),
        ),
    ]
