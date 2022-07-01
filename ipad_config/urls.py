# Django Imports
from django.urls import path

# Project imports
from ipad_config import views, import_views, api_views, hotel_views

urlpatterns = [

    # Add hotel
    path("add/", views.add_hotel, name="add_hotel"),

    # Hotel details
    path("<int:hotel_id>/", views.hotel_details, name="hotel_details"),

    # fqdns
    path("<int:hotel_id>/fqdns/", views.fqdns, name="fqdns"),
    path("<int:hotel_id>/sync_fqdns/", views.sync_fqdn, name="sync_fqdns"),

    # Language and codes
    path("<int:hotel_id>/language_list/", views.hotel_language_list, name="hotel_language_list"),
    path("<int:hotel_id>/hotel_language/add/", views.hotel_language_edit, name="hotel_langauge_add"),
    path("<int:hotel_id>/hotel_language/<int:language_id>/edit/", views.hotel_language_edit,
         name="hotel_language_edit"),
    path("<int:hotel_id>/hotel_language/<int:language_id>/delete/", views.hotel_language_delete,
         name="hotel_language_delete"),

    path("<int:hotel_id>/language_code_list/", views.hotel_language_code_list, name="hotel_language_code_list"),
    path("<int:hotel_id>/hotel_language_code/add/", views.hotel_language_code_edit, name="hotel_langauge_code_add"),
    path("<int:hotel_id>/hotel_language_code/<int:language_code_id>/edit/", views.hotel_language_code_edit,
         name="hotel_language_code_edit"),
    path("<int:hotel_id>/hotel_language_code/<int:language_code_id>/delete/", views.hotel_language_code_delete,
         name="hotel_language_code_delete"),

    # Ariport details
    path("<int:hotel_id>/hotel_airportdetails_list/", views.hotel_airportdetail_list, name="hotel_airportdetail_list"),
    path("<int:hotel_id>/hotel_airportdetails/add/", views.hotel_airportdetail_edit, name="hotel_airportdetail_add"),
    path("<int:hotel_id>/hotel_airportdetails/<int:airport_id>/edit/", views.hotel_airportdetail_edit,
         name="hotel_airportdetail_edit"),
    path("<int:hotel_id>/hotel_airportdetails/<int:airport_id>/delete/", views.hotel_airportdetail_delete,
         name="hotel_airportdetail_delete"),

    # Hotel image
    path("<int:hotel_id>/hotel_image_list/", views.hotel_image_list, name="hotel_image_list"),
    path("<int:hotel_id>/hotel_image/add/", views.hotel_image_edit, name="hotel_image_add"),
    path("<int:hotel_id>/hotel_image/<int:image_id>/edit/", views.hotel_image_edit, name="hotel_image_edit"),

    # Hotel static content
    path("<int:hotel_id>/hotel_staticcontent_list/", views.hotel_staticcontent_list, name="hotel_staticcontent_list"),
    path("<int:hotel_id>/hotel_staticcontent/add/", views.hotel_staticcontent_edit, name="hotel_staticcontent_add"),
    path("<int:hotel_id>/hotel_staticcontent/<int:staticcontent_id>/edit/", views.hotel_staticcontent_edit,
         name="hotel_staticcontent_edit"),
    path("<int:hotel_id>/hotel_staticcontent/<int:staticcontent_id>/delete/", views.hotel_staticcontent_delete,
         name="hotel_staticcontent_delete"),

    # Hotel splash images
    path("<int:hotel_id>/splash_image/list/", hotel_views.splash_image_list, name="splash_image_list"),
    path("<int:hotel_id>/splash_image/add/", hotel_views.splash_image_edit, name="splash_image_add"),
    path("<int:hotel_id>/splash_image/<int:image_id>/edit/", hotel_views.splash_image_edit, name="splash_image_edit"),
    path("<int:hotel_id>/splash_image/<int:image_id>/delete/", hotel_views.splash_image_delete,
         name="splash_image_delete"),

    # Hotel java config
    path("<int:hotel_id>/java_configs/", hotel_views.java_config_list, name="java_configs_list"),
    path("<int:hotel_id>/export_java_config/", hotel_views.export_java_config, name="export_java_config"),
    path("<int:hotel_id>/java_configs/add/", hotel_views.add_java_config, name="java_config_add"),
    path("<int:hotel_id>/java_configs/edit/<int:config_id>/", hotel_views.add_java_config, name="java_config_edit"),
    path("<int:hotel_id>/java_configs/unsync_all/", hotel_views.unsync_java_configs, name="unsync_java_configs"),
    path("<int:hotel_id>/java_configs/show_changes/", hotel_views.show_import_changes, name="show_import_changes"),
    path("<int:hotel_id>/java_configs/sync_from_default/", hotel_views.sync_from_default, name="sync_from_default"),

    # Hotel ipad profile menu
    path("<int:hotel_id>/ipad_profiles/", hotel_views.ipad_profiles, name="ipad_profiles_list"),
    path("<int:hotel_id>/ipad_profile/add/", hotel_views.add_ipad_profile, name="ipad_profile_add"),
    path("<int:hotel_id>/ipad_profile/edit/<int:profile_id>/", hotel_views.edit_ipad_profile, name="ipad_profile_edit"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/", hotel_views.ipad_profile_view, name="ipad_profile_view"),

    # ipad profile feature settings
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/feature_settings/", hotel_views.feature_settings_list,
         name="feature_settings_list"),

    # ipad profile home feature settings
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/home_feature_settings/", hotel_views.home_feature_settings_list,
         name="home_feature_settings_list"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/home_feature_settings/add/",
         hotel_views.home_feature_setting_edit, name="home_feature_settings_add"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/home_feature_settings/<int:setting_id>/edit/",
         hotel_views.home_feature_setting_edit, name="home_feature_settings_edit"),

    # ipad profile common feature settings
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/common_settings/", hotel_views.common_settings_list,
         name="common_settings_list"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/common_settings/add/", hotel_views.common_settings_edit,
         name="common_settings_add"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/common_settings/<int:setting_id>/edit/",
         hotel_views.common_settings_edit, name="common_settings_edit"),

    # ipad profile main feature settings
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_settings/<int:setting_id>/edit",
         hotel_views.main_feature_settings_edit, name="main_feature_settings_edit"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_settings/add",
         hotel_views.main_feature_settings_edit, name="main_feature_settings_add"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_settings/<int:setting_id>/settings",
         hotel_views.main_feature_settings_settings, name="main_feature_settings_settings"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_settings/", hotel_views.main_feature_settings_list,
         name="main_feature_settings_list"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_settings/<int:setting_id>/images",
         hotel_views.main_feature_images, name="main_feature_images"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_images/<int:setting_id>/<int:image_id>/edit",
         hotel_views.main_feature_image_edit, name="main_feature_image_edit"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/main_feature_setting_images/<int:setting_id>/add",
         hotel_views.main_feature_image_edit, name="main_feature_image_add"),
    path("ipad_profile/main_feature_setting_images/<int:setting_id>/delete/<int:image_id>",
         hotel_views.delete_main_feature_image, name="delete_main_feature_image"),

    # ipad profile hotel services and mapping
    path("ipad_profile/<int:profile_id>/hotel_services/", hotel_views.hotel_services_list, name="hotel_services_list"),
    path("ipad_profile/<int:profile_id>/hotel_services/add/", hotel_views.hotel_services_edit,
         name="hotel_services_add"),
    path("ipad_profile/<int:profile_id>/hotel_services/<int:service_id>/edit/", hotel_views.hotel_services_edit,
         name="hotel_services_edit"),
    path("hotel_services/<int:service_id>/mapping/", hotel_views.hotel_services_mapping_list,
         name="hotel_services_mapping_list"),
    path("hotel_services/<int:hotel_service_id>/add/", hotel_views.hotel_services_mapping_edit,
         name="hotel_services_mapping_add"),
    path("hotel_services/<int:hotel_service_id>/mapping/<int:mapping_id>/edit/",
         hotel_views.hotel_services_mapping_edit, name="hotel_services_mapping_edit"),
    path("hotel_services/<int:hotel_service_id>/mapping/<int:mapping_id>/delete/",
         hotel_views.hotel_services_mapping_delete, name="hotel_services_mapping_delete"),

    # Export changes
    path("export_ipad_configuration/<int:profile_id>/", views.export_ipad_configuration,
         name="export_ipad_configuration"),
    path("<int:hotel_id>/ipad_profile_export/<int:profile_id>/", hotel_views.ipad_profile_export,
         name="ipad_profile_export"),

    # Hotel publish queue
    path("<int:hotel_id>/publish_queue/", views.publish_queue, name="publish_queue"),
    path("<int:hotel_id>/show_publish_changes/<int:queue_id>", views.show_publish_changes, name="show_publish_changes"),
    path("<int:hotel_id>/ipad_profile/<int:profile_id>/profile_queue/", hotel_views.profile_queue,
         name="profile_queue"),

    # User actions
    path("add_profile/", views.add_profile, name="add_profile"),
    path("edit_profile/<int:profile_id>/", views.edit_profile, name="edit_profile"),
    path("delete_profile/<int:profile_id>/", views.delete_profile, name="delete_profile"),
    path("confirm_delete_profile/<int:profile_id>/", views.confirm_delete_profile, name="confirm_delete_profile"),
    path("config_profile/<int:profile_id>/", views.config_profile, name="config_profile"),
    path("select_features/", views.select_features, name="select_features"),
    path("feature_ordering/<int:profile_id>/", views.feature_ordering, name="feature_ordering"),
    path("download/<str:type>/", views.index, name="download"),

    # Import feature
    path("import_seed/", views.import_seed, name="import_seed"),
    path("import_language_seed/", views.import_language_seed, name="import_language_seed"),
    path("<int:hotel_id>/import_hotel_language_code/", views.import_hotel_language_code,
         name="import_hotel_language_code"),
    path("<int:hotel_id>/import_hotel_language/", views.import_hotel_language, name="import_hotel_language"),
    path("import_seed_sql/", views.import_seed_sql, name="import_seed_sql"),
    path("import_main_features/", views.import_main_features, name="import_main_features"),
    path("import_common_settings/", views.import_common_settings, name="import_common_settings"),
    path("import_features_setting/", views.import_features_setting, name="import_features_setting"),
    path("import_home_features/", views.import_home_features, name="import_home_features"),
    path("import_asset_zip/", views.import_asset_zip, name="import_asset_zip"),

    # Other utils
    path("dgjava/", views.dgjava, name="dgjava"),
    path("generate_dgjava/", views.generate_dgjava, name="generate_dgjava"),
    path("java_env_varialble/<int:id>/", views.edit_java_env_variable, name="java_env_varialble"),
    path("appconfig/", views.appconfig, name="appconfig"),
    path("splash_images/<int:profile_id>/", views.splash_images, name="splash_images"),
    path("download/<str:type>/", views.index, name="index"),
    path("import_seed/", views.import_seed, name="import_seed"),
    path("<str:profile>/settings_images/assets.json", views.assets_json, name="assets_json"),
    path("get_content/<str:hotel_code>/", views.get_content, name="get_content"),
    path("get_java_configs/<str:hotel_code>/", api_views.JavaConfigList.as_view(), name="get_java_configs"),
    path("ack_java_configs_sync/<str:hotel_code>/", api_views.ack_java_configs_sync, name="ack_java_configs_sync"),
    path("import_java_config_json/", import_views.import_java_config_json, name="import_java_config_json"),
    path("sync_fqdn/<str:hotel_code>/", api_views.SyncFqdn.as_view(), name="sync_fqdn"),
    path("import_home_service_defaults/<int:hotel_id>/", import_views.import_home_service_defaults,
         name="import_home_config_defaults"),

]
