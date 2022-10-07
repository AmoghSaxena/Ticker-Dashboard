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
    path('delete/history/<str:id>', views.isDeleteHistory, name = 'deleteHistory'),
    path('detail/<str:id>', views.detail, name = 'detail'),
    path('accounts/changepassword/', views.changePassword, name = 'changepassword'),
    path('abort/<str:id>', views.abort, name = 'abort'),

    ####  Logs ####
    path('system/info/logs/', views.systemLog, name = 'systemLog'),
    path('system/celery/beat/logs/', views.celeryBeatLog, name = 'celeryBeatLog'),
    path('system/celery/worker/logs/', views.celeryWorkerLog, name = 'celeryWorkerLog'),

    #### API's
	path('ticker-post', views.taskPost),
    path('ticker-config-api', views.configApi),
    path('java/reboot/status',views.rebootStatus,name='rebootStatus'),
    path('java/tv-ipad/status',views.tvIpadStatus,name='tvipadStatus'),
    path('java/status/close',views.statusClose,name='statusClose'),
    path('java/dnd',views.dndStatus,name='dndStatus'),
    path('priority-ticker',views.checkPriorityTicker,name='checkPriorityTicker'),
    path('close-ticker',views.closeTicker,name='closeTicker'),
    # path('tickerStatusReboot/',views.tickerStatusReboot),
]