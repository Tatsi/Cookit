from django.db import models

class Recipe(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    image_url = models.CharField(max_length=600)
    steps = models.CharField(max_length=10000, blank=True)
    # TODO creator
    # TODO ingredients
    rating_count = models.BigIntegerField()
    average_rating = models.DecimalField(max_digits=10, decimal_places=9)