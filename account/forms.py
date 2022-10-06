from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from account.models import Profile
from django.forms.widgets import PasswordInput, TextInput


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if len(username) < 3:
            raise forms.ValidationError('Minimum 4 characters required.')
        return username

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and len(password1) < 5 and len(password2) < 5:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
            raise forms.ValidationError("Password length should be greater than 5.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@gmail.com' not in email or '@yahoo.com' not in email:
            raise forms.ValidationError("Please enter valid email address.")
        return email




class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['display_name', 'image', 'bio']