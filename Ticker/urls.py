"""Ticker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('initiate.urls')),
    # path('', views.index, name = 'index'),
    # path('createticker', views.createticker, name = 'createticker'),
    # path('active', views.active, name = 'active'),
    # path('pending', views.pending, name = 'pending'),
    # path('history', views.history, name = 'history'),
    # path('preview', views.preview, name = 'preview'),
    # path('schedule', views.schedule, name = 'schedule'),
    # path('', views.login, name = 'login')
]
