from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.forms import RegisterForm

def mainpage(request):
	context = {}
	return render(request, 'mainpage.html', context)

def feed(request):
	array = []
	for i in range(5):
		array.append({'title': 'Pea soup a la Otaniemi '+str(i), 'stars': '1'*i+'0'*(5-i), 'description': 'This is a delicious pea soup featuring goose liver. Exeptionally well suited for quick lounches.'})
	context = {'recipes': array}
	return render(request, 'feed.html', context)

def recipe(request):
	name = 'Chicken soup'
	favourite = True
	username = 'Mary_1982'
	description = 'Pure soul food, this warming, easy chicken soup makes the most of leftover roast chicken.'
	time = '1 h'
	servings = 6
	ingredients = [
		{'amount': '55 g', 'name': 'butter'},
		{'amount': '2', 'name': 'onions'},
		{'amount': '2 sticks', 'name': 'celery'},
		{'amount': '2', 'name': 'carrots'},
		{'amount': '25 g', 'name': 'flour'},
		{'amount': '450 g', 'name': 'chicken'},
		{'amount': '1 tbsp', 'name': 'parsley'},
		{'amount': '1 tsp', 'name': 'black pepper'},
	]
	instructions = [
		'Melt the butter in a large saucepan over a medium heat and gently fry the onions, celery and carrots until they start to soften.',
		'Stir in the flour and cook for 2 minutes. Add the chicken stock and bring the mixture to the boil, stirring as you do so. Season with salt and pepper, then reduce the heat until the mixture is simmering and simmer for 10 minutes, until the vegetables are tender.',
		'Add the cooked chicken and cook until heated through. Adjust the seasoning, stir in the parsley and serve.',
		'Eat'
	]
	context = {
		'name': name,
		'favourite': favourite,
		'username': username,
		'description': description,
		'time': time,
		'servings': servings,
		'ingredients': ingredients,
		'instructions': instructions,
	}
	return render(request, 'recipe.html', context)

def new_recipe(request):
    context = {}
    return render(request, 'new_recipe.html', context)

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data["username"], email=form.cleaned_data["email"],
			                                    password=form.cleaned_data["password"])
			return HttpResponseRedirect(reverse('mainpage'))
	else:
	    form = RegisterForm()
	return render(request, "registration/register.html", {"form": form})