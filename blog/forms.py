from pyexpat import model
from django import forms
from django.forms import ModelForm
import re
from blog.models import Post,ContactUs
from account.models import User
from tinymce.widgets import TinyMCE


class PostForm(ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 25}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'category',  'author', 'image']


# class ContactForm(forms.Form):
    # countries = [("IND", "INDIA"), ("CHN", "China")]
    # name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "input-field", "placeholder": "Name"}))
    # # password = forms.CharField(max_length=16, widget=forms.PasswordInput)
    # email = forms.EmailField(required=False,widget=forms.TextInput(attrs={"placeholder": "Your Email"}))
    # phone = forms.RegexField(regex="^[6-9][0-9]{9}$", label="Phone", error_messages={"invalid": "Please provide valid indian phone number."}, required=False,widget=forms.TextInput(attrs={"placeholder": "Your Mobile No."}))
    # message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"placeholder": "Your Message"}))
    # country = forms.ChoiceField(choices=countries)

class ContactForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
# def clean(self):
#     cleaned_data = super().clean()
#     email = cleaned_data.get("email")
#     phone = cleaned_data.get("phone_number")

#     if email == "" and phone == "":
#         raise forms.ValidationError("Atleast email or phone number should be provided", code="Invalid")


def clean_password(self):
    password = self.cleaned_data.get("password")
    m = re.search("[A-Z]", password)
    if not m:
        raise forms.ValidationError("Atleast one uppercase", code="upper")
    else:
        return password





