# Create your views here.
# Import necessary modules and models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# Define a view function for the home page
def home(request):
    return render(request, 'home.html')

# Define a view function for the login page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            # Ensure a Profile exists for the logged in user
            Profile.objects.get_or_create(user=user)
            return redirect('/dashboard/')  # Redirect to dashboard

    return render(request, 'login.html')

# Define a view function for the registration page
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        # Create Profile for new user immediately after registration
        Profile.objects.get_or_create(user=user)
        
        messages.info(request, "Account created successfully!")
        return redirect('/login/')  # Redirect to login after registration

    return render(request, 'register.html')

# Define a view function for the dashboard page
@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    # Get or create profile safely
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        if 'profile_pic' in request.FILES:
            profile.profile_image = request.FILES['profile_pic']
            profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')

    return render(request, 'profile.html', {'user': request.user, 'profile': profile})
