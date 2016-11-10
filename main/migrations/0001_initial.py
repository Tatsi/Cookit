# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-07 11:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('ingredient_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('unit_short', models.CharField(max_length=10)),
                ('unit', models.CharField(max_length=20)),
                ('unit_long', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=500)),
                ('default_amount', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('servings', models.IntegerField()),
                ('duration', models.DurationField()),
                ('image_url', models.CharField(max_length=600)),
                ('steps', models.CharField(blank=True, max_length=10000)),
                ('rating_count', models.BigIntegerField()),
                ('average_rating', models.DecimalField(decimal_places=9, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=100)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourite_recipes', models.ManyToManyField(related_name='main_useraccount_favourites', to='main.Recipe')),
                ('favourite_users', models.ManyToManyField(related_name='_useraccount_favourite_users_+', to='main.UserAccount')),
                ('history_recipes', models.ManyToManyField(related_name='main_useraccount_history', to='main.Recipe')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserAccount'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='main.RecipeIngredient', to='main.Ingredient'),
        ),
    ]