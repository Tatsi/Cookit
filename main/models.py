from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    # id = models.BigIntegerField(primary_key=True) # Not needed
    title = models.CharField(max_length=300)
    image_url = models.CharField(max_length=600)
    steps = models.CharField(max_length=10000, blank=True)
    # TODO creator
    # TODO ingredients
    rating_count = models.BigIntegerField()
    average_rating = models.DecimalField(max_digits=10, decimal_places=9)

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO favourite recipes
    # TODO favourite users
    # TODO history_recipes

class Ingredient(models.Model):
    ingredient_id = models.BigIntegerField(primary_key=True)
    unit_short = models.CharField(max_length=10)
    unit = models.CharField(max_length=20)
    unit_long = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    default_amount = models.CharField(max_length=100)