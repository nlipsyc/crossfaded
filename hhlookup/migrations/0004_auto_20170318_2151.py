# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhlookup', '0003_song_old_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='slug',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='song',
            name='slug',
            field=models.TextField(default=''),
        ),
    ]