from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView,UpdateView
from account.forms import SignUpForm, ProfileUpdateForm
from blog.models import Post
from account.models import Profile
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


class UserCreateView(CreateView):
    template_name = "account/signup.html"
    form_class = SignUpForm
    success_url = "/blogs"


    

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