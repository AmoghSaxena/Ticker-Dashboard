from . import views
from django.urls import path
from django.contrib import admin
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .views import RegisterView
urlpatterns = [
    path('', views.index, name = 'index'),
    path('createticker', views.createticker, name = 'createticker'),
    path('active', views.active, name = 'active'),
    path('pending', views.pending, name = 'pending'),
    path('history', views.history, name = 'history'),
    path('preview', views.preview, name = 'preview'),
    path('schedule', views.schedule, name = 'schedule'),
    path('registerform',views.registerfor,name='registerform'),
    path('register',RegisterView.as_view(), name='register'),
    # url(r'^login/$', login, {'template_name': 'admin/login.html'})
    # path('login', views.login, name = 'login')
    path('accounts/login/', views.login, name = 'login')
]