
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Product
from django.http import JsonResponse
import json

products = Product.objects.all()

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
    return render(request, 'registration/ready_to_grab.html',{'products':products})

def cooked_to_serve(request):
    return render(request, 'registration/cooked_to_serve.html',{'products':products})

def beverages(request):
    return render(request, 'registration/beverages.html',{'products':products})

def menu(request):
    # Initialize cart count from session
    cart_count = sum(request.session.get('cart', {}).values())
    return render(request, 'menu.html', {'cart_count': cart_count})

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        # Get or initialize cart in session
        cart = request.session.get('cart', {})
        cart[item_id] = cart.get(item_id, 0) + 1
        
        # Save updated cart to session
        request.session['cart'] = cart
        return JsonResponse({
            'status': 'success',
            'cart_count': sum(cart.values())
        })
    return JsonResponse({'status': 'error'}, status=400)

def cart_2(request):
    cart = request.session.get('cart', {})
    cart_items = []
    
    # Sample item database (replace with your actual model)
    ITEM_DB = {
        '1': {'name': 'Veg Meals', 'price': 80},
        '2': {'name': 'Sambar Rice', 'price': 70},
        # Add all other items similarly...
    }
    
    total = 0
    for item_id, quantity in cart.items():
        item = ITEM_DB.get(item_id)
        if item:
            item_total = item['price'] * quantity
            cart_items.append({
                'id': item_id,
                'name': item['name'],
                'price': item['price'],
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': total,
        'discount': total * 0.05,
        'total': total * 0.95
    })


def snacks(request):
    return render(request, 'registration/snacks.html',{'products':products})

def sidedish(request):
    return render(request, 'registration/sidedish.html',{'products':products})