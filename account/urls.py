from django.urls import path, include
from account.views import register_user, login_view, logout_user, profile_page_view, UpdateProfileView, change_password
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,PasswordChangeDoneView


urlpatterns = [
    
    path('signup/', register_user, name="signup"),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    # path('', include('django.contrib.auth.urls')),
    # path('login/',  auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    
    path('profile/', profile_page_view, name='profile'),
    # path('profile/<int:pk>', profile, name="ProfileUpdate"),
    path('profile/<int:pk>', UpdateProfileView.as_view(), name="ProfileUpdate"),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('password-change/', change_password, name='change_password'),
#     path('password-change/done/', PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),

]