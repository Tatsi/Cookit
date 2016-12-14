from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_recipes = models.ManyToManyField('Recipe', related_name="%(app_label)s_%(class)s_favourites")
    favourite_users = models.ManyToManyField('self')
    cooked_recipes = models.ManyToManyField('Recipe', through='CookedRecipe')
    ingredients = models.ManyToManyField('Ingredient', through='UserIngredient')
    description = models.CharField(max_length=100000, blank=True)

class Recipe(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    servings = models.IntegerField()
    duration = models.DurationField()
    #image_url = models.CharField(max_length=600)
    steps = models.CharField(max_length=10000, blank=True)
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    rating_count = models.BigIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=10, decimal_places=9, default=0)
    #image = models.ImageField(upload_to='images')
    creation_date = models.DateField((u"Creation Date"), auto_now_add=True, blank=True)
    creation_time = models.TimeField((u"Creation Time"), auto_now_add=True, blank=True)

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe)
    image = models.ImageField(upload_to='recipeimages')

class UserImage(models.Model):
    user_account = models.ForeignKey(UserAccount)
    image = models.ImageField(upload_to='userimages')

class CookedRecipe(models.Model):
    recipe = models.ForeignKey(Recipe)
    user_account = models.ForeignKey(UserAccount)
    cooking_date = models.DateField((u"Cooking Date"), auto_now_add=True, blank=True)
    cooking_time = models.TimeField((u"Cooking Time"), auto_now_add=True, blank=True)
    serving_count = models.IntegerField()

class Ingredient(models.Model):
    ingredient_id = models.BigIntegerField(primary_key=True) # ID from external API
    unit_short = models.CharField(max_length=10)
    unit = models.CharField(max_length=20)
    unit_long = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    default_amount = models.CharField(max_length=100)
    class Meta:
        ordering = ['name']

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=100)

class UserIngredient(models.Model):
    user_account = models.ForeignKey(UserAccount)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=100)
    infinite = models.BooleanField(default=False)



