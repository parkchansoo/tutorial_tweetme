# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-29 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.CharField(default='tweet anyting', max_length=140),
        ),
    ]
