# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20161115_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='description',
            field=models.CharField(blank=True, max_length=100000),
        ),
    ]
