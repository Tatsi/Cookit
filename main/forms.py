from django import forms
from django.contrib.auth.models import User

class IngredientsForm(forms.Form):
	ingredient = forms.CharField(max_length=80, required=True)

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(max_length=100, required=True)
	password = forms.CharField(max_length=100, required=True)
	password_re = forms.CharField(max_length=100, required=True)

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