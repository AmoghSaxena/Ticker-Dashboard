from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = 'index'),
    path('createticker/', views.createticker, name = 'createticker'),
    path('active/', views.active, name = 'active'),
    path('pending/', views.pending, name = 'pending'),
    path('history/', views.history, name = 'history'),
    path('preview/<str:id>/', views.preview, name = 'preview'),
    path('schedule/<str:id>/', views.schedule, name = 'schedule'),
    path('accounts/login/', views.login, name = 'login')
]