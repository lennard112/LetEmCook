# lecApp/urls.py
from django.urls import path
from . import views

app_name = 'lecApp'

urlpatterns = [
    path('', views.welcome_page, name='welcome'),  # Home page
    path('login/', views.login_page, name='login'),  # Login page
    path('register/', views.register_page, name='register'),  # Register page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page after login
    path('email_mfa/', views.email_mfa_view, name='email_mfa'),  # Email MFA page
]
