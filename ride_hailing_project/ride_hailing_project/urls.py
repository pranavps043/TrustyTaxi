from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Django default admin site (optional)
    path('admin_side/', include('admin_side.urls')),  # Your custom admin side
    path('', include('user_side.urls')),  # User side as default root
]
