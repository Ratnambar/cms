from django.conf import settings
from email import message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from account.models import Profile
from django.forms.widgets import PasswordInput, TextInput
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


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


    def send_mail(request):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        if subject and message and from_email :
            try:
                send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return HttpResponse("Email has been sent.")
        else:
            return HttpResponse("Make sure all fields are correct.")





class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['display_name', 'image', 'bio']