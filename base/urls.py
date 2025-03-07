from django.urls import path, include
from .views import authView, home


urlpatterns = [
 path("", home, name="home"),
 path("signup/", authView, name="auth"),
 path("accounts/", include("django.contrib.auth.urls")),
]