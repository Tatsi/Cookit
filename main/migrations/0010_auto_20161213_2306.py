# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20161213_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'userimages')),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserAccount')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipeimage',
            name='user_account',
        ),
        migrations.AddField(
            model_name='recipeimage',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Recipe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipeimage',
            name='image',
            field=models.ImageField(upload_to=b'recipeimages'),
        ),
    ]
