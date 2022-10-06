from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views.generic import CreateView,UpdateView
from account.forms import SignUpForm, ProfileUpdateForm
from blog.models import Post
from account.models import Profile

from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
# Create your views here.


class UserCreateView(CreateView):
    template_name = "account/signup.html"
    form_class = SignUpForm
    success_url = "/blogs"


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


