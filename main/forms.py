from django import forms
from django.contrib.auth.models import User

# Form for submitting new recipes
class NewRecipeForm(forms.Form):
	title = forms.CharField()
	description = forms.CharField()
	steps = forms.CharField(required=False) # Takes steps in JSON format?
	ingredients = forms.CharField(required=False) # Takes ingredients in JSON format?
	servings = forms.IntegerField()
	hours = forms.IntegerField(required=False, initial=0) 
	minutes = forms.IntegerField(required=False, initial=0)

	def clean(self):
		if not "hours" in self.cleaned_data and not "minutes" in self.cleaned_data:
			self.add_error("minutes", forms.ValidationError("Enter the duration!"))
		return self.cleaned_data

# Form for filtering recipes based on ingredients user has
class IngredientsForm(forms.Form):
	ingredient = forms.CharField(max_length=100)
	delete = forms.BooleanField(required=False)

# Form for user account registration
class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)
	password = forms.CharField(max_length=100)
	password_re = forms.CharField(max_length=100)

	def clean_password(self):
	    data = self.cleaned_data["password"]
	    if len(data) < 8:
	        raise forms.ValidationError("Password too short! (Minimum: 8 characters)")
	    return data

	def clean_email(self):
	    data = self.cleaned_data["email"]
	    if User.objects.filter(email=data).exists():
	        raise forms.ValidationError("Email already in use!")
	    return data

	def clean(self):
	    password1 = None
	    password2 = None
	    if "password" in self.cleaned_data:
	        password1 = self.cleaned_data["password"]
	    if "password_re" in self.cleaned_data:
	        password2 = self.cleaned_data["password_re"]
	    if password1 and password1 != password2:
	        self.add_error("password_re", forms.ValidationError("Passwords don't match!"))
	    return self.cleaned_data