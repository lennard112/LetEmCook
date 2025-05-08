# lecApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def welcome_page(request):
    return render(request, 'lecApp/welcome.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'lecApp/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            # Generic error message to prevent account enumeration (security best practice)
            messages.error(request, 'Invalid username or password.')
            return render(request, 'lecApp/login.html')

    return render(request, 'lecApp/login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'lecApp/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'lecApp/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'lecApp/register.html')

        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'lecApp/register.html')

@login_required
def dashboard(request):
    return render(request, 'lecApp/dashboard.html')
