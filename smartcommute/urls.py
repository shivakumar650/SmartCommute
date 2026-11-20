"""
URL configuration for smartcommute project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.urls import include
from commute import views as commute_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', commute_views.home, name='home'),
    path('about/', commute_views.about, name='about'),
    path('devices/', commute_views.device_list, name='devices'),
    path('devices/<int:device_id>/', commute_views.device_detail, name='device_detail'),
    path('innovation/', commute_views.innovation, name='innovation'),
    path('contact/', commute_views.contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('commute/', include('commute.urls')),
    path('analytics/', include('analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
