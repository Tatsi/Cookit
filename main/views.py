from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from main.forms import RegisterForm, IngredientsForm, NewRecipeForm
from main.models import Ingredient, UserAccount, UserIngredient, Recipe, RecipeIngredient
from django.utils import dateparse
import json

def mainpage(request):
	context = {}
	return render(request, 'mainpage.html', context)

def feed(request):
	# dummy implementation of recipes
	array = []
	for i in range(5):
		array.append({'title': 'Pea soup a la Otaniemi '+str(i), 'author': 'user123', 'stars': '1'*i+'0'*(5-i), 'description': 'This is a delicious pea soup featuring goose liver. Exeptionally well suited for quick lounches.', 'id': i})
	context = {'recipes': array}

	if request.user.is_authenticated():
		user_acc = UserAccount.objects.get(user=request.user)

		if request.method == 'POST':
			form = IngredientsForm(request.POST)
			if form.is_valid():
				try:
					ingredient = Ingredient.objects.get(name=form.cleaned_data['ingredient'])
				except Ingredient.DoesNotExist:
					pass
				else:
					item = UserIngredient.objects.filter(user_account=user_acc, ingredient=ingredient)
					if not form.cleaned_data['delete']:
						if not item.exists():
							user_ingredient = UserIngredient.objects.create(user_account=user_acc, ingredient=ingredient, amount='1')
					else:
						if item.exists():
							item.delete()
		else:
			form = IngredientsForm()

		# Convert all ingredients to a list and pass to template
		context['all_ingredients'] = list(Ingredient.objects.all().values_list('name', flat=True))

		# Fetch ingredients the user has
		context['my_ingredients'] = user_acc.ingredients.all()

	# TODO: Update the filter and return the list of matching recipes
	return render(request, 'feed.html', context)

def recipe(request, recipe_id):
	# Get recipe from db
	try:
		recipe = Recipe.objects.get(id=recipe_id)
	except Recipe.DoesNotExist:
		raise Http404("No Recipe found for ID %s.".format(recipe_id))

	# Check if the user has this recipe in his favourites
	user = request.user
	user_account = UserAccount.objects.get(user=user)
	try:
		user_account.favourite_recipes.get(id=recipe_id)
	except Recipe.DoesNotExist:
		favourite = False
	else:
		favourite = True

	# Parse duration
	duration = recipe.duration
	seconds = duration.seconds
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)

	# Parse steps
	steps = json.loads(recipe.steps)

	# Filter ingredients
	ingredients = RecipeIngredient.objects.filter(recipe=recipe)

	context = {
		'name': recipe.title,
		'favourite': favourite,
		'creator': recipe.creator,
		'description': recipe.description,
		'time': {'hours': hours, 'minutes': minutes},
		'servings': recipe.servings,
		'ingredients': ingredients,
		'instructions': steps,
		'ratings': recipe.rating_count,
		'average_rating': recipe.average_rating,
	}
	return render(request, 'recipe.html', context)

def new_recipe(request):
	if request.method == 'POST':
		form = NewRecipeForm(request.POST)
		if form.is_valid():
			# Dummy. Now we just print the data to console
			# TODO: Save the recipe to DB
			print(form.cleaned_data['title'])
			print(form.cleaned_data['description'])
			print(form.cleaned_data['servings'])
			timedelta = str(form.cleaned_data['hours']) + ':' + str(form.cleaned_data['minutes']) + ':0'
	else:
		form = NewRecipeForm()
	context = {}
	return render(request, 'new_recipe.html', context)

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data["username"], email=form.cleaned_data["email"],
												password=form.cleaned_data["password"])
			new_user_account = UserAccount.objects.create(user=new_user)
			return HttpResponseRedirect(reverse('mainpage'))
	else:
		form = RegisterForm()
	return render(request, "registration/register.html", {"form": form})