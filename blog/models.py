from django.db import models
from django.contrib.auth.models import User
from account.models import Profile
from django.urls import reverse
from django.utils.text import slugify
from tinymce import models as tinymce_models
from django.utils.timezone import now

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    statuses = [
        ("D", "Draft"),
        ("P", "Published"),
    ]
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)
    content = tinymce_models.HTMLField()
    status = models.CharField(max_length=1, choices=statuses)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/post", blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'sno': self.sno})

    def update_reverse_path(self):
        return reverse('update-blog', kwargs={'slug': self.slug})

    def delete_reverse_path(self):
        return reverse('delete-blog', kwargs={'slug': self.slug})


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:20]+"..."+"by "+self.user.username


class ContactUs(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=11, blank=False)
    message = models.TextField()

    def __str__(self):
        return self.name
