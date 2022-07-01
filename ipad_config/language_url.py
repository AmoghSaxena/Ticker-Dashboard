"""
Created on 28-Dec-2019

@author: sumit-rathore
"""

# Django Imports
from django.urls import path

# Project Imports
from ipad_config import language_views

urlpatterns = [
    path("dv_language_code/add/", language_views.dv_language_code_edit, name="dv_language_code_add"),
    path("dv_language_code/<int:language_code_id>/edit/", language_views.dv_language_code_edit,
         name="dv_language_code_edit"),
    path("dv_language_code/<int:language_code_id>/delete/", language_views.dv_language_code_delete,
         name="dv_language_code_delete"),
    path("dv_language/add/", language_views.dv_language_edit, name="dv_language_add"),
    path("dv_language/<int:language_id>/edit/", language_views.dv_language_edit, name="dv_language_edit"),
    path("dv_language/<int:language_id>/delete/", language_views.dv_language_delete, name="dv_language_delete"),
]
