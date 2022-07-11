from . import views
from django.urls import path

urlpatterns = [
    path('accounts/login/', views.login, name = 'login'),
    path('', views.index, name = 'index'),
    path('createticker/', views.createTicker, name = 'createticker'),
    path('updateticker/<str:id>', views.updateTicker, name = 'updateticker'),
    path('active/', views.active, name = 'active'),
    path('history/', views.history, name = 'history'),
    path('scheduled/', views.scheduled, name = 'scheduled'),
    path('restore/<str:id>', views.isRestore, name = 'restore'),
    path('delete/<str:id>', views.isDelete, name = 'delete'),
    path('preview/<str:id>/', views.preview, name = 'preview'),
	path('ticker-post/', views.taskPost),
    path('ticker-config-api/', views.configApi)
]