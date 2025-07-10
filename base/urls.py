from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name='home'),  # Handles /
    path("home/", views.home, name='home'),  # Handles /home/
    path("login/", views.custom_login, name="login"),
    path('logout/', views.custom_logout , name='logout'),
    path("signup/", views.authView, name="auth"),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('ready-to-grab/', views.ready_to_grab, name='ready_to_grab'),
    path('cooked-to-serve/', views.cooked_to_serve, name='cooked_to_serve'),
    path('beverages/', views.beverages, name='beverages'),
    path('snacks/', views.snacks, name='snacks'),
    path('sidedish/', views.sidedish, name='sidedish'),
    path('contact/', views.contact, name='contact'),



]
