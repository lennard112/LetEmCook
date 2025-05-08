from django.contrib import admin
from django.urls import path, include
from lecApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome_page, name='welcome'),  # Home page
    path('login/', views.login_page, name='login'),  # Login page
    path('register/', views.register_page, name='register'),  # Register page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page after login
    path('accounts/', include('allauth.urls')),  # Social account login urls
]
