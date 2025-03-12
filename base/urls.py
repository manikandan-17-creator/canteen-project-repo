from django.urls import path, include
from .views import authView, home,custom_login,update_profile
from django.contrib.auth.views import LogoutView



urlpatterns = [
 path("", home, name="home"),
 path("login/", custom_login, name="login"),
 path('logout/', LogoutView.as_view(), name='logout'),  
 path("signup/", authView, name="auth"),
 path('update-profile/', update_profile, name='update_profile'),
 
 ]
