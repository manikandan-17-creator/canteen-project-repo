
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile 


@login_required
def home(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    profile_picture = request.user.profile.profile_picture.url if request.user.profile.profile_picture else None
    return render(request, 'registration/home.html', {'profile_picture': profile})

@login_required
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'registration/update_profile.html', {'form': form})


def authView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST.get('password2')

            # Check if a user with the same email already exists
            if User.objects.filter(username=email).exists():
                messages.error(request, 'A user with this email already exists. Please use a different email.')
                return render(request, 'registration/signup.html', {'form': form})  # Return to signup page with error

            # Check if passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'registration/signup.html', {'form': form})  # Return to signup page with error

            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password1)

            # Create a profile for the new user
            Profile.objects.get_or_create(user=user)

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid email or password.')
            return redirect('login')  # Redirect back to the login page
    else:
        return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)  # This clears the session
    return redirect('login')  # Redirect to the login page (URL name must be 'login')

def ready_to_grab(request):
    return render(request, 'registration/ready_to_grab.html')

def cooked_to_serve(request):
    return render(request, 'registration/cooked_to_serve.html')

def beverages(request):
    return render(request, 'registration/beverages.html')