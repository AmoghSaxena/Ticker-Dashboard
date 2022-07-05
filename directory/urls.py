"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""
from django.conf.urls import include
try:
    from django.conf.urls import url
except ImportError:
    from . import views
    from django.urls import path

from directory import views

urlpatterns = (
    path(r'^(?P<path>.*)$', views.browse, name='directory_browse'),
)
