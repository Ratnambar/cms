
from multiprocessing import context
from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from blog.forms import ContactForm
from blog.forms import PostForm
from django.views import View
from blog.models import Post, Category, ContactUs,BlogComment
from account.models import User,Profile
from django.views.generic import ListView,CreateView, DetailView,FormView, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy,reverse
from blog.templatetags import extras





def indexPage(request,*args,**kwargs):
    posts = Post.objects.all()
   
    return render(request, "blog/index.html", context={"posts": posts})


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # context['author'] = Author.objects.all()
        return context


class PostFormView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'login'
    # model = Post
    permission_required = 'blog.add_post'
    template_name = 'blog/post.html'
    form_class = PostForm


class PostFormUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'login'
    permission_required = 'blog.change_post'
    model = Post
    form_class = PostForm
    template_name = "blog/post.html"

    def test_func(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        # author = User.post_set.get(slug=slug)
        # print(post)
        # print(self.__dict__)
        # print(args)
        # print(kwargs)
        post = Post.objects.get(slug=slug)
        if self.request.user.get_username() == post.author.user.get_username():
            return True
        else:
            return False

  

class PostFormDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('profile')
    template_name = "blog/confirm-delete.html"
  


def search_code(request):
    search_term = ""
    articles = []
    if 'search' in request.GET:
        search_term = request.GET.get('search')
        posts = Post.objects.all()
        for post in posts:
            if search_term.lower() in post.title.lower() or search_term in post.title.lower():
                print(search_term)
                print(post.title)
                articles.append(post)
        return render(request, "blog/search.html", context={'articles': articles})
    else:
        return render(request, "blog/search.html")


def view_by_cat_button(request, id):
    category = Category.objects.all()
    posts = Post.objects.filter(category__id=id)
    context = {
        'category': category,
        'posts': posts
        }
    return render(request, 'blog/cat_views.html', context)




def BtnBlogDetails(request, slug):
    post = Post.objects.filter(slug=slug).first()
    total_like = get_object_or_404(Post,slug=slug)
    total_likes = total_like.total_likes()
    comments = BlogComment.objects.filter(post=post)
    context = {'post': post, 'user': request.user,'total_likes':total_likes,'comments':comments}
    return render(request, 'blog/btn-details.html',context)


def post_details_view(request, sno):
    post = Post.objects.filter(sno=sno).first()
    total_like = get_object_or_404(Post, sno=sno)
    total_likes = total_like.total_likes()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print(replyDict)
    context = {'post': post, 'user': request.user,'total_likes':total_likes,'comments':comments,'replyDict':replyDict}
    return render(request, 'blog/details.html', context)



def like_post(request,sno):
    post = Post.objects.get(sno=sno)
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail',args=[int(request.POST.get('post_sno'))]))



def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        parentSno = request.POST.get("parentSno")
        post = Post.objects.get(sno=postSno)

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            # messages.success(request,"Your comment has been posted successfully.")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post,parent=parent)
            comment.save()
            # messages.success(request,"Your reply has been posted successfully.")
        return redirect(f"/blogs/{postSno}")



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect(f"/blogs/contact/")
        form = ContactForm()
        context = {'form':form}
        return render(request, 'blog/contact.html', context)
    return render(request, 'blog/contact.html', context={"form": ContactForm})




def Trending_Posts(request):
    trending_posts = Trending_Posts.objects.all()
    print(trending_posts)
    return render(request, "blog/index.html", context={"trending_posts": trending_posts})


def post_edit_form_view(request,id,*args,**kwargs):
    try:
        post = Post.objects.get(id=id)
    except:
        return HttpResponse("Invalid Post ID")

    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, "blog/post.html", context={"form": form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponse("welcome")

        return render(request, "blog/post.html", context={"form": form})
    return render(request, "blog/post.html", context={"form": form})



