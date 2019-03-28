from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length = 100, required = True)
	last_name = forms.CharField(max_length = 100, required = True)
	email = forms.EmailField(max_length = 254, help_text = 'eg. ksarthak4ever@gmail.com') #defining some fields attributes for UserCreationForm i.e Optional

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2') #fields to be shown in the form
