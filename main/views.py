from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.forms import RegisterForm

def mainpage(request):
	context = {}
	return render(request, 'mainpage.html', context)


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