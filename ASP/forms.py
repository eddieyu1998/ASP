from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer.')
    last_name = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer.')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', )