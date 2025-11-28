
from http.client import HTTPResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView,UpdateView,  FormView
from account.forms import SignUpForm, LoginForm, ProfileUpdateForm
from blog.models import Post
from account.models import Profile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import HttpResponse
# Create your views here.


# class UserCreateView(CreateView):
#     template_name = "account/signup.html"
#     form_class = SignUpForm
#     success_url = "/blogs"


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            login(request, user)
            messages.success(request, "Successfully registered.")
            return redirect('index')
        else:
            messages.error(request, "check the credentials.")
    else:
        form = SignUpForm()
        return render(request, 'account/signup.html',{'form':form})


def login_view(request):
    if request.user.is_authenticated:
        for key,value in request.session.items():
            print(value)
        return redirect("index")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['username'] = username
            messages.success(request, "loggedin successfully.")
            return redirect("index")
            return render(request, "blog/base.html",{'user':user})
        else:
            messages.error(request, "can't login")
            # form = LoginForm(request.POST)
            # return render(request, "account/login.hml", {'form':form})
    else:
        form = LoginForm()
        return render(request, "account/login.html",{'form':form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def profile_page_view(request):
    user = request.user.id
    # users = User.objects.get(id=user)
    profiles = Profile.objects.get(user_id=user)
    posts = Post.objects.filter(author=profiles)
    print(profiles)
    context = {
        'profiles': profiles,
        'posts': posts,
    }
    return render(request, 'account/profile.html', context)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "account/profile_update.html"
    success_url = reverse_lazy('profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password has been changed")
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html',{'form': form})