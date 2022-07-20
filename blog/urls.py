from django.urls import path, re_path
# from blog.views import index
from blog.views import indexPage,PostListView,PostFormView,search_code,view_by_cat_button,BtnBlogDetails, contact, post_edit_form_view,post_details_view,like_post,PostFormUpdateView,PostFormDeleteView,postComment


urlpatterns = [
    # path("index", indexPage),
    path("", PostListView.as_view(template_name="blog/index.html"), name="index"),
    # path("postComment", postComment, name='postComment'),
    path("posts", PostFormView.as_view(template_name="blog/post.html"), name="post"),
    # path("posts", post_form_view),
    path("search/", search_code, name="search"),
    path("contact/", contact, name="contact"),
    path("like/<int:sno>", like_post, name="like_post"),
    path("<int:sno>", post_details_view, name="post-detail"),
    path("filter/<int:id>", view_by_cat_button),
    path("filter/<slug:slug>", BtnBlogDetails),
    path("posts/<slug:slug>", PostFormUpdateView.as_view(), name="update-blog"),
    path("delete/<slug:slug>", PostFormDeleteView.as_view(),name="delete-blog"),
    path('comment', postComment, name="postComment"),
]