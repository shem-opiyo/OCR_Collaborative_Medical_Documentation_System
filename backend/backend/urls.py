"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, UserListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/list/', UserListView.as_view(), name='list-users'),

    path('api/patients/', include('patients.urls')), 
    path('api/departments/', include('departments.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/records/', include('medical_records.urls')),
    path('api/image-processing/', include('document_processing.urls')),
    path('api/audio-processing/', include('audio_processing.urls')),
    path('api/text-processing/', include('text_processing.urls')),

]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    