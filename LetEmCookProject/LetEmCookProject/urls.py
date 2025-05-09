from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lecApp.urls', namespace='lecApp')),  # 👈 Include lecApp with namespace
    path('accounts/', include('allauth.urls')),  # Social auth
]
