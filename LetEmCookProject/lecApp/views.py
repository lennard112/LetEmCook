from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def welcome_page(request):
    return render(request, 'lecApp/welcome.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'lecApp/login.html')  # Render login page if credentials are incorrect

    return render(request, 'lecApp/login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Validation: ensure all fields are filled
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'lecApp/register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'lecApp/register.html')

        # Optional: Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'lecApp/register.html')

        # Create the user
        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')  # Redirect to login page

    return render(request, 'lecApp/register.html')

def dashboard(request):
    return render(request, 'lecApp/dashboard.html')  # Render dashboard page
