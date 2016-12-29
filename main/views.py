from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from main.forms import RegisterForm, IngredientsForm, NewRecipeForm, SettingsForm
from main.models import Ingredient, UserAccount, UserIngredient, Recipe, RecipeIngredient, CookedRecipe, RecipeImage, UserImage, RatedRecipe
from django.utils import dateparse
import json, datetime, random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def mainpage(request):
	context = {}
	user = request.user
	if user.is_authenticated():
		#user_account = UserAccount.objects.get(user=user)
		# Fetch ingredients the user has
		#context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)
		#context['all_ingredients'] = json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))
		return HttpResponseRedirect(reverse('feed'))

	# Get 6 random recipes
	ids = Recipe.objects.values_list('id', flat=True)
	n = 6
	rand_ids = random.sample(ids, n)
	recipes = Recipe.objects.filter(id__in=rand_ids)

	# Add images of each recipe to context
	images = []
	for recipe in recipes:
		images = RecipeImage.objects.filter(recipe=recipe)
		if images:
			recipe.image = images[0]

	context['recipes'] = recipes
	context['message'] = "We are embarrassed, no recipes were found.."
	return render(request, 'mainpage.html', context)

def search(request):
	search_query = request.GET.get('searchQuery')
	context = {}
	context['search_query'] = search_query
	recipes = Recipe.objects.filter(title__contains=search_query)

	context['recipes'] = recipes
	#print context['recipes']
	return render(request, 'search.html', context)

def feed(request, feed_type=None):
	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	message = "There is no recipes"

	if feed_type is None:
		if not user.is_authenticated():
			recipes = Recipe.objects.all()
		else:
			recipes = Recipe.objects.filter(ingredients__in=user_account.ingredients.all()).distinct()
			message = "There is no recipes matching your own ingredients"
	else:
		if user.is_authenticated():
			if feed_type == "own_recipes":
				recipes = Recipe.objects.filter(creator=user_account)
				message = "You can create your own recipes by clicking 'New Recipe'! They will show up here."
			elif feed_type == "favourites":
				recipes = user_account.favourite_recipes.all()
				message = "You can mark recipes as your favourites by clicking heart button next to recipe title. Favourite recipes will show up here."
			elif feed_type == "history":
				cooked_recipes = CookedRecipe.objects.filter(user_account=user_account).order_by('-cooking_date', '-cooking_time')
				recipes = [cooked.recipe for cooked in cooked_recipes]
				message = "You have not cooked anything yet. You can add recipes to your cooking history by clicking 'COOKIT' button in recipe page."
			else:
				raise Http404()
		else:
			raise Http404()

	if user.is_authenticated():
		for recipe in recipes:
			if recipe in user_account.favourite_recipes.all():
				recipe.favourite = True

	# Add images of each recipe to context
	images = []
	for recipe in recipes:
		images = RecipeImage.objects.filter(recipe=recipe)
		if images:
			recipe.image = images[0]

	context = {'recipes': recipes}
	context['message'] = message

	if user.is_authenticated():
		# Convert all ingredients to a list and pass to template
		context['all_ingredients'] = json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))
		# Fetch ingredients the user has
		context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)

	# TODO: Update the filter and return the list of matching recipes
	return render(request, 'feed.html', context)

def user(request, user_id=None):
	if user_id is None:
		raise Http404()

	viewed_user = User.objects.get(id=user_id)
	viewed_user_account = UserAccount.objects.get(user=viewed_user)

	recipes = Recipe.objects.filter(creator=viewed_user_account)
	context = {'recipes': recipes, 'viewed_user': viewed_user, 'viewed_user_account': viewed_user_account}

	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	images = UserImage.objects.filter(user_account=viewed_user_account)

	context['user'] = user
	context['images'] = images

	if user.is_authenticated():
		if viewed_user_account in user_account.favourite_users.all():
			context['favourite_user'] = True

		# Convert all ingredients to a list and pass to template
		context['all_ingredients'] = json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))

		# Fetch ingredients the user has
		context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)

	return render(request, 'user.html', context)

@login_required
def settings(request):
	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	if request.method == "POST":
		form = SettingsForm(request.POST, instance=user_account)
		if form.is_valid():
			form.save()

			# Store new image
			request_images = request.FILES.getlist('image')
			for img in request_images:
				#print "Saving user profile image.."
				image = UserImage(user_account=user_account, image=img)
				image.save()
				# print "done!"
				# print "url: " + image.image.url
				# print "path: " + image.image.path
				# print "name: " + image.image.name
				break
			#print "redirecting"
			#return redirect('user', user_id=user.id)

			# Remove images
			removed_images = request.POST.getlist('removeimage')
			for img_id in removed_images:
				#print "Removing userimage  " + str(img_id)
				image = UserImage.objects.get(id=img_id)
				image.delete()
				#print "Removed userimage " + str(img_id)
	else:
		form = SettingsForm()

	images = UserImage.objects.filter(user_account=user_account)
	context = {'user': user, 'user_account': user_account, 'images': images}

	if user.is_authenticated():
		# Convert all ingredients to a list and pass to template
		context['all_ingredients'] = json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))

		# Fetch ingredients the user has
		context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)

	if len(images) > 0:
		context['hasUserImage'] = True

	return render(request, 'settings.html', context)

@login_required
def add_my_ingredient(request):
	user = request.user

	if user.is_authenticated():
		user_account = UserAccount.objects.get(user=user)
		if request.method == 'POST':
			form = IngredientsForm(request.POST)
			if form.is_valid():
				name = form.cleaned_data['ingredient_name']
				amount = form.cleaned_data['ingredient_amount']
				try:
					# TODO: Ingredients should not contain many ingredients with the same name
					# This is only in the demo phase
					ingredients = Ingredient.objects.filter(name=name)
				except Ingredient.DoesNotExist:
					pass
				else:
					item = UserIngredient.objects.filter(user_account=user_account, ingredient__in=ingredients)
					if not form.cleaned_data['delete']:
						if not item.exists():
							user_ingredient = UserIngredient.objects.create(user_account=user_account, ingredient=ingredients[0], amount=amount)
					else:
						if item.exists():
							item.delete()
			else:
				pass
				#print form.errors
		else:
			form = IngredientsForm()

		return HttpResponse('')


def recipe(request, recipe_id):
	# Get recipe from db
	try:
		recipe = Recipe.objects.get(id=recipe_id)
	except Recipe.DoesNotExist:
		raise Http404("No Recipe found for ID %s.".format(recipe_id))

	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	user_rating = None

	# Check if the user has this recipe in his favourites
	if user_account:
		try:
			user_account.favourite_recipes.get(id=recipe_id)
		except Recipe.DoesNotExist:
			favourite = False
		else:
			favourite = True
		try:
			rated_recipe = RatedRecipe.objects.get(recipe=recipe, user_account=user_account)
		except RatedRecipe.DoesNotExist:
			pass
		else:
			user_rating = rated_recipe.user_rating
	else:
		favourite = False

	# Parse duration
	duration = recipe.duration
	seconds = duration.seconds
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)

	# Parse steps
	steps = json.loads(recipe.steps)

	# Filter ingredients
	ingredients = RecipeIngredient.objects.filter(recipe=recipe)

	# Filter images
	images = RecipeImage.objects.filter(recipe=recipe)
	#print images

	# Create absolute url
	absolute_url = request.build_absolute_uri()

	# Was the recipe just saved? (for showing alert)
	saved = request.GET.get('saved', False)

	context = {
		'saved': saved,
		'recipe': recipe,
		'favourite': favourite,
		'time': {'hours': hours, 'minutes': minutes},
		'ingredients': ingredients,
		'instructions': steps,
		'images': images,
		'user_rating': user_rating,
		'absolute_url': absolute_url,
		'all_ingredients': json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))
	}

	if user.is_authenticated():
		# Fetch ingredients the user has
		context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)

	return render(request, 'recipe.html', context)

def has_cooked(recipe, user_account):
	if CookedRecipe.objects.filter(user_account=user_account, recipe=recipe).count() > 0:
		return True
	else:
		return False

@login_required
@csrf_exempt
def rate_recipe(request):
	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None
	if request.method == "POST":
		rating = float(request.POST.get("rating"))
		recipe_id = request.POST.get("id")
		try:
			recipe = Recipe.objects.get(id=recipe_id)
		except Recipe.DoesNotExist:
			return JsonResponse({'code': 1, 'message': 'Recipe not found'})
		else:
			if has_cooked(recipe, user_account):
				try:
					rated_recipe = RatedRecipe.objects.get(recipe=recipe, user_account=user_account)
				except RatedRecipe.DoesNotExist:
					r_recipe = RatedRecipe.objects.create(recipe=recipe, user_account=user_account, user_rating=rating)
					# Update average rating
					recipe.average_rating = (float(recipe.average_rating)*recipe.rating_count + rating)/(recipe.rating_count+1)
					recipe.rating_count += 1
					recipe.save()
					return JsonResponse({'code': 0, 'message':'Voting succesful', 'rating': recipe.average_rating})
				else:
					# Update average rating
					recipe.average_rating = float(recipe.average_rating) + (rating - rated_recipe.user_rating)/recipe.rating_count
					recipe.save()
					rated_recipe.user_rating = rating
					rated_recipe.save()
					return JsonResponse({'code': 0, 'message':'Rating changed', 'rating': recipe.average_rating})
			else:
				return JsonResponse({'code': 2, 'message':'You have to Cookit before rating'})

		return JsonResponse({'code': 0, 'message':'Voting succesful', 'rating': recipe.average_rating})

@login_required
def cook_recipe(request, recipe_id):
	# Get recipe from db
	try:
		recipe = Recipe.objects.get(id=recipe_id)
	except Recipe.DoesNotExist:
		raise Http404("No Recipe found for ID %s.".format(recipe_id))

	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	if request.method == "POST":
		if user_account:
			servings = request.POST.get("servings")
			CookedRecipe.objects.create(
				recipe = recipe,
				user_account = user_account,
				serving_count = servings
			)

			# Decrease my ingredient amount according to recipe ingredient amounts
			recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
			user_ingredients = UserIngredient.objects.filter(user_account=user_account)
			ingredients = [ingredient.ingredient for ingredient in user_ingredients]
			for i in range(0, len(recipe_ingredients)-1):
				if recipe_ingredients[i].ingredient in ingredients:
					user_ingredient = user_ingredients.get(ingredient=recipe_ingredients[i].ingredient)
					# The amount should be defined by the selected servings
					new_recipe_amount = float(recipe_ingredients[i].amount) / int(recipe.servings) * int(servings)
					new_amount = float(user_ingredient.amount) - float(new_recipe_amount)
					if new_amount >= 0:
						# Set the new amount
						user_ingredient.amount = new_amount
						user_ingredient.save()
					else:
						# Delete ingredient
						user_ingredient.delete()

			return JsonResponse({'code': 0, 'message':'Recipe cooked'})

# @login_required
# def upload_recipe_image(request, recipe_name):
# 	if request.method == "POST":
# 		recipe = Recipe.objects.get(id=recipe_id)
# 		form = RecipeImageForm(request, recipe=recipe_id)
# 		if form.is_valid():
# 			#form = form.save(commit=False)
# 			#form.user = request.user
# 			form.save()
# 			# return redirect('user', user_id=user.id)
# 	else:
# 		return HttpResponse('')

@login_required
def add_favourite(request, recipe_id):
	# Get recipe from db
	try:
		recipe = Recipe.objects.get(id=recipe_id)
	except Recipe.DoesNotExist:
		raise Http404("No Recipe found for ID %s.".format(recipe_id))

	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	if request.method == "POST":
		if user_account:
			try:
				user_account.favourite_recipes.get(id=recipe_id)
			except Recipe.DoesNotExist:
				user_account.favourite_recipes.add(recipe)
			else:
				user_account.favourite_recipes.remove(recipe)
			return HttpResponse('')

@login_required
def add_favourite_user(request, user_id):
	# Get user from db
	try:
		favourite_user = UserAccount.objects.get(id=user_id)
	except Recipe.DoesNotExist:
		raise Http404("No User Account found for ID %s.".format(user_id))

	user = request.user
	user_account = UserAccount.objects.get(user=user) if user.is_authenticated() else None

	if request.method == "POST":
		if user_account:
			try:
				user_account.favourite_users.get(id=user_id)
			except UserAccount.DoesNotExist:
				user_account.favourite_users.add(user_id)
			else:
				user_account.favourite_users.remove(user_id)
			return HttpResponse('')

@login_required
def new_recipe(request):
	if request.method == 'POST':
		#print "request:"
		#print request.POST

		form = NewRecipeForm(request.POST)

		if form.is_valid():
			hours = form.cleaned_data['hours']
			if hours == None:
				hours = 0
			minutes = form.cleaned_data['minutes']
			if minutes == None:
				minutes = 0

			data = {
				'title': 		form.cleaned_data['title'],
				'description':	form.cleaned_data['description'],
				'servings':		form.cleaned_data['servings'],
				'steps':		form.cleaned_data['steps'],
				'duration':		datetime.timedelta(hours=hours, minutes=minutes),
				'creator':		UserAccount.objects.get(user=request.user)
			}
			recipe = Recipe.objects.create(**data)

			# Store images
			request_images = request.FILES.getlist('image')

			for img in request_images:
				#print "Saving image "
				image = RecipeImage(recipe=recipe, image=img)
				image.save()
				# print "done."
				# print "url: " + image.image.url
				# print "path: " + image.image.path
				# print "name: " + image.image.name

			# Add the ingredients
			ingredients = json.loads(form.cleaned_data['ingredients'])
			for item in ingredients:
				ingredient = Ingredient.objects.filter(name=item[0])[0]
				r_ingredient = RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=item[1])
			return JsonResponse({"id": recipe.id})

	else:
		form = NewRecipeForm()
	context = {}
	context['all_ingredients'] = json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))

	user = request.user
	user_account = UserAccount.objects.get(user=user)

	# Fetch ingredients the user has
	context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)

	return render(request, 'new_recipe.html', context)

@login_required
def edit_recipe(request, recipe_id):
	# Get recipe from db
	try:
		recipe = Recipe.objects.get(id=recipe_id)
	except Recipe.DoesNotExist:
		raise Http404("No Recipe found for ID %s.".format(recipe_id))

	user = request.user
	user_account = UserAccount.objects.get(user=user)

	# If recipe is not user's own, return 403
	if user_account != recipe.creator:
		return HttpResponseForbidden("You have no permission to edit this recipe.")

	if request.method == "POST":
		form = NewRecipeForm(request.POST)
		if form.is_valid():
			hours = form.cleaned_data['hours']
			if hours == None:
				hours = 0
			minutes = form.cleaned_data['minutes']
			if minutes == None:
				minutes = 0

			data = {
				'title': 		form.cleaned_data['title'],
				'description':	form.cleaned_data['description'],
				'servings':		form.cleaned_data['servings'],
				'steps':		form.cleaned_data['steps'],
				'duration':		datetime.timedelta(hours=hours, minutes=minutes),
				'creator':		UserAccount.objects.get(user=request.user)
			}
			Recipe.objects.filter(id=recipe.id).update(**data)

			# Get old ingredients
			old_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
			new_ingredients = json.loads(form.cleaned_data['ingredients'])

			# If ingredients are not in new ingredients, delete them
			found = False
			for old_ingredient in old_ingredients:
				for new_ingredient in new_ingredients:
					if old_ingredient.ingredient.name == new_ingredient[0]:
						found = True
					found = False

				if found is False:
					old_ingredient.delete()

			# Remove removed images
			removed_images = request.POST.getlist('removeimage')
			for img_id in removed_images:
				#print "Removing image  " + str(img_id)
				image = RecipeImage.objects.get(id=img_id)
				image.delete()
				#print "Removed image " + str(img_id)

			# Store new images
			request_images = request.FILES.getlist('image')

			for img in request_images:
				#print "Saving image "

				image_count = RecipeImage.objects.filter(recipe=recipe).count()
				#print image_count
				if image_count < 5:
					image = RecipeImage(recipe=recipe, image=img)
					image.save()
					# print "done."
					# print "url: " + image.image.url
					# print "path: " + image.image.path
					# print "name: " + image.image.name
				else:
					break

			# Update or create new ingredients
			for item in new_ingredients:
				ingredient = Ingredient.objects.filter(name=item[0])[0]
				try:
					recipe_ingredient = RecipeIngredient.objects.get(recipe=recipe, ingredient=ingredient)
					RecipeIngredient.objects.filter(id=recipe_ingredient.id).update(amount=item[1])
				except RecipeIngredient.DoesNotExist:
					RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=item[1])

			return HttpResponse('')
	else:
		form = NewRecipeForm()

	# Filter ingredients
	ingredients = RecipeIngredient.objects.filter(recipe=recipe)

	# Filter images
	images = RecipeImage.objects.filter(recipe=recipe)

	# Parse duration
	duration = recipe.duration
	seconds = duration.seconds
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)

	# Parse steps
	steps = json.loads(recipe.steps)

	# Was the recipe just saved? (for showing alert)
	saved = request.GET.get('saved', False)

	context = {}
	context['saved'] = saved
	context['recipe'] = recipe
	context['ingredients'] = ingredients
	context['images'] = images
	context['time'] = {'hours': hours, 'minutes': minutes}
	context['steps'] = steps
	context['all_ingredients'] = json.dumps(list(Ingredient.objects.all().values('name', 'unit', 'unit_short').distinct()))

	# Fetch ingredients the user has
	context['my_ingredients'] = UserIngredient.objects.filter(user_account=user_account)

	return render(request, 'new_recipe.html', context)

@login_required
def remove_recipe(request, recipe_id):
	# Get recipe from db
	try:
		recipe = Recipe.objects.get(id=recipe_id)
	except Recipe.DoesNotExist:
		raise Http404("No Recipe found for ID %s.".format(recipe_id))

	user = request.user
	user_account = UserAccount.objects.get(user=user)

	# If recipe is not user's own, return 403
	if user_account != recipe.creator:
		return HttpResponseForbidden("You have no permission to remove this recipe.")

	# Delete decipe
	recipe.delete()

	return HttpResponse('')

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