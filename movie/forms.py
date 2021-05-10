from django.forms import ModelForm, TextInput
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'Movie Name'})}


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateListForm(ModelForm):
    class Meta:
        model = MovieList
        fields = '__all__'
        exclude = ['user_name']




