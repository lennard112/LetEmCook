# LetEmCookProject/urls.py
from django.contrib import admin
from django.urls import path, include
from lecApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome_page, name='welcome'),  # Redirect to welcome page
    path('login/', views.login_page, name='login'),  # Login page route
    path('register/', views.register_page, name='register'),  # Registration page route
    path('accounts/', include('allauth.urls')),  # Include allauth routes
    
]
