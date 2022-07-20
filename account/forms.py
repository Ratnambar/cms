from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from account.models import Profile
from django.forms.widgets import PasswordInput, TextInput


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['display_name', 'image', 'bio']