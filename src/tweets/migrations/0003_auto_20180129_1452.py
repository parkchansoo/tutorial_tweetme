# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-29 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import tweets.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20180129_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.CharField(default='tweet anyting', max_length=140, validators=[tweets.validators.validate_content]),
        ),
    ]
