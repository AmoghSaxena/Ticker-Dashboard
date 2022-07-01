"""
Created on 28-Dec-2019

@author: sumit-rathore
"""

from django.urls import path


from ipad_config import theme_views

urlpatterns = [
    path("home/", theme_views.theme_home, name="theme_home"),
    path("add/", theme_views.add_theme, name="add_theme"),
    path("edit/<int:theme_id>/", theme_views.add_theme, name="edit_theme"),


    # font styles
    path("font_styles/<int:theme_id>/", theme_views.font_style_list, name="font_styles"),
    path("<int:theme_id>/font_style/edit/<int:font_style_id>/", theme_views.add_font_style, name="font_style_edit"),
    path("<int:theme_id>/font_style/add/", theme_views.add_font_style, name="font_style_add"),

    path("font_style_mappings/<int:theme_id>/", theme_views.font_style_mapping_list, name="font_style_mappings"),
    path("<int:theme_id>/font_style_mapping/edit/<int:font_style_mapping_id>/", theme_views.add_font_style_mapping, name="font_style_mapping_edit"),
    path("<int:theme_id>/font_style_mapping/add/", theme_views.add_font_style_mapping, name="font_style_mapping_add"),

    # color styles add_font_style_mapping
    path("<int:theme_id>/setting_assets/list/", theme_views.setting_assets_list, name="setting_assets_list"),
    path("<int:theme_id>/setting_assets/add/", theme_views.setting_assets_edit, name="setting_assets_add"),
    path("<int:theme_id>/setting_assets/<int:asset_id>/edit/", theme_views.setting_assets_edit, name="setting_assets_edit"),
    path("<int:theme_id>/setting_asset/<int:asset_id>/delete/", theme_views.setting_asset_delete, name="setting_asset_delete"),
    path("<int:theme_id>/setting_asset/bulk_delete/", theme_views.setting_asset_bulkdelete, name="setting_asset_bulkdelete"),

    path("color_styles/<int:theme_id>/", theme_views.color_style_list, name="color_styles"),
    path("<int:theme_id>/color_style/edit/<int:color_style_id>/", theme_views.add_color_style, name="color_style_edit"),
    path("<int:theme_id>/color_style/add/", theme_views.add_color_style, name="color_style_add"),

    path("color_style_mappings/<int:theme_id>/", theme_views.color_style_mapping_list, name="color_style_mappings"),
    path("<int:theme_id>/color_style_mapping/edit/<int:color_style_mapping_id>/", theme_views.add_color_style_mapping, name="color_style_mapping_edit"),
    path("<int:theme_id>/color_style_mapping/add/", theme_views.add_color_style_mapping, name="color_style_mapping_add"),

    path("airlines/", theme_views.airline_list, name="airlines"),
    path("airlines/edit/<int:airline_id>/", theme_views.airline_edit, name="airline_edit"),
    path("airlines/delete/<int:airline_id>/", theme_views.airline_delete, name="airline_delete"),
    path("airlines/add/", theme_views.airline_edit, name="airline_add"),

    path("airport_detail/", theme_views.airport_detail_list, name="airport_detail_list"),
    path("airport_detail/edit/<int:airport_id>/", theme_views.airport_detail_edit, name="airport_detail_edit"),
    path("airport_detail/delete/<int:airport_id>/", theme_views.airport_detail_delete, name="airport_detail_delete"),
    path("airport_detail/add/", theme_views.airport_detail_edit, name="airport_detail_add"),
    path("import_airport_details/", theme_views.import_airport_details, name="import_airport_details"),

    path("import_airline_details/", theme_views.import_airline_details, name="import_airline_details"),

    path("<int:theme_id>/", theme_views.theme_details, name="theme_details"),
    path("<int:theme_id>/export_asset_zip", theme_views.export_asset_zip, name="export_asset_zip")


]
