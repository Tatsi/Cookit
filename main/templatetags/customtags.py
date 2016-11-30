from django import template
from main.models import Ingredient

register = template.Library()

@register.filter
def full_stars(value):
    return range(int(round(value)))

@register.filter
def empty_stars(value):
    return range(5-int(round(value)))
    