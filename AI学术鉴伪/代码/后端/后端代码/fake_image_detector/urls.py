"""fake_image_detector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.static import serve
import sys

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('core.urls')),
]

from django.conf import settings

# runserver 调试环境下，即使 DEBUG=False 也允许直接访问 media。
if settings.DEBUG or 'runserver' in sys.argv:
    media_prefix = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += [
        re_path(rf'^{media_prefix}/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]