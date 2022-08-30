from . import views
from django.urls import path

urlpatterns = [
    path('accounts/login/', views.login, name = 'login'),
    path('', views.index, name = 'index'),
    path('createticker/', views.createTicker, name = 'createticker'),
    path('active/', views.active, name = 'active'),
    path('history/', views.history, name = 'history'),
    path('scheduled/', views.scheduled, name = 'scheduled'),
    path('updateticker/<str:id>', views.updateTicker, name = 'updateticker'),
    path('edit/<str:id>', views.isEdit, name = 'edit'),
    path('restore/<str:id>', views.isRestore, name = 'restore'),
    path('delete/<str:id>', views.isDelete, name = 'delete'),
    path('detail/<str:id>', views.detail, name = 'detail'),
    path('accounts/changepassword/', views.changePassword, name = 'changepassword'),
    path('abort/<str:id>', views.abort, name = 'abort'),
	path('ticker-post/', views.taskPost),
    path('ticker-config-api/', views.configApi),
    path('java/ticker/reboot/status/',views.rebootStatus,name='rebootStatus'),
    path('java/ticker/tv-ipad/status/',views.tvIpadStatus,name='tvipadStatus'),
    path('java/ticker/status/close/',views.statusClose,name='statusClose'),
    # path('tickerStatusReboot/',views.tickerStatusReboot),
]