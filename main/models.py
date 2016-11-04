from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourites_recipes = models.ManyToManyField('Recipe', related_name="%(app_label)s_%(class)s_favourites")
    favourite_users = models.ManyToManyField('self')
    history_recipes = models.ManyToManyField('Recipe', related_name="%(app_label)s_%(class)s_history")

class Recipe(models.Model):
    # id = models.BigIntegerField(primary_key=True) # Not needed
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    servings = models.IntegerField()
    duration = models.DurationField()
    image_url = models.CharField(max_length=600)
    steps = models.CharField(max_length=10000, blank=True)
    creator = models.ForeignKey(UserAccount)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    rating_count = models.BigIntegerField()
    average_rating = models.DecimalField(max_digits=10, decimal_places=9)

class Ingredient(models.Model):
    ingredient_id = models.BigIntegerField(primary_key=True) # ID in external API
    unit_short = models.CharField(max_length=10)
    unit = models.CharField(max_length=20)
    unit_long = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    default_amount = models.CharField(max_length=100)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=100)



