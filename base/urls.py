from django.urls import path
from .views import authView, home, custom_login, update_profile,ready_to_grab,cooked_to_serve,beverages,custom_logout
urlpatterns = [
    path("", home, name='home'),  # Handles /
    path("home/", home, name='home'),  # Handles /home/
    path("login/", custom_login, name="login"),
    path('logout/', custom_logout , name='logout'),
    path("signup/", authView, name="auth"),
    path('update-profile/', update_profile, name='update_profile'),
    path('ready-to-grab/', ready_to_grab, name='ready_to_grab'),
    path('cooked-to-serve/', cooked_to_serve, name='cooked_to_serve'),
    path('beverages/', beverages, name='beverages'),
]
