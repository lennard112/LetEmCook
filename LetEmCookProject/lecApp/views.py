# lecApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta, timezone as std_timezone  # Import standard timezone

import random

# ------------------ Existing views ------------------

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
            return redirect('lecApp:email_mfa')  # **Using the correct namespace here!**
        else:
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
            return render(request, 'lecApp/login.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'lecApp/login.html')

        User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('lecApp:login')  # Use the correct namespaced URL here

    return render(request, 'lecApp/register.html')

@login_required
def dashboard(request):
    # Only allow if MFA has been passed
    if not request.session.get('email_mfa_passed'):
        return redirect('lecApp:email_mfa')  # Use the correct namespaced URL here
    return render(request, 'lecApp/dashboard.html')

# ------------------ Email MFA views ------------------

@login_required
def email_mfa_view(request):
    user = request.user

    # Initialize MFA session vars
    if 'email_mfa_code' not in request.session or is_code_expired(request):
        generate_and_send_email_code(request, user)

    if request.method == 'POST':
        entered_code = request.POST.get('code', '').strip()

        if entered_code == request.session.get('email_mfa_code') and not is_code_expired(request):
            request.session['email_mfa_passed'] = True
            clear_mfa_session(request)
            messages.success(request, 'Email verification successful!')
            return redirect('lecApp:dashboard')  # Use the correct namespaced URL here
        else:
            messages.error(request, 'Invalid or expired code. Please try again.')
            return render(request, 'lecApp/email_mfa.html')

    return render(request, 'lecApp/email_mfa.html')

# ------------------ Helper functions ------------------

def generate_6_digit_code():
    return '{:06d}'.format(random.randint(0, 999999))

def generate_and_send_email_code(request, user):
    code = generate_6_digit_code()
    request.session['email_mfa_code'] = code
    request.session['email_mfa_created_at'] = timezone.now().isoformat()

    send_mail(
        'Your Let Em Cook Verification Code',
        f'Your verification code is: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

def is_code_expired(request):
    created_at_str = request.session.get('email_mfa_created_at')
    if not created_at_str:
        return True
    created_at = datetime.fromisoformat(created_at_str)  # Use datetime's fromisoformat
    created_at = created_at.replace(tzinfo=std_timezone.utc)  # Ensure timezone-aware
    return timezone.now() > created_at + timedelta(minutes=5)

def clear_mfa_session(request):
    request.session.pop('email_mfa_code', None)
    request.session.pop('email_mfa_created_at', None)
