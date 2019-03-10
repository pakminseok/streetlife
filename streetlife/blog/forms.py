from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Enter password here'}))
	confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Confirm password'}))
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
		]

	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password != confirm_password:
			raise forms.ValidationError('Password Mismatch')
		return confirm_password

class UserLoginForm(forms.Form):
	username = forms.CharField(label="")
	password = forms.CharField(label="", widget=forms.PasswordInput)
