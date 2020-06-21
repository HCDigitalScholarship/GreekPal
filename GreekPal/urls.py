"""GreekPal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from greek_app.views import logout_view
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from greek_app import views
from django.contrib.flatpages import views as flat_views
from django.contrib.auth import logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('browse/', views.home, name='browse'),
    path('symbol-json/', views.SymbolJson.as_view(), name='symbol_json'),
]

# flat pages 
urlpatterns += [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('about/', flat_views.flatpage, {'url': '/about/'}, name='about'),
]

# Social auth
urlpatterns += [
    path('', include('social_django.urls', namespace='social')),
    path('logout/', views.logout_view, name='logout'),
]
