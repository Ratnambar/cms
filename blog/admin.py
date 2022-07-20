from django.contrib import admin
from blog.models import Post

from blog.models import Category,ContactUs,BlogComment

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title','content')


# Register your models here.
admin.site.register(Post)
admin.site.register(Category),
admin.site.register(ContactUs),
admin.site.register(BlogComment),

