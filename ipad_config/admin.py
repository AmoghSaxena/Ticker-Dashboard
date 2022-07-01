# Python Imports
import os

# Django Imports
from django.contrib import admin
from django.forms import widgets

# Project Imports
from .models import *
from config.settings.base import MEDIA_ROOT

admin.site.register(RoomType)
admin.site.register(Hotel)
admin.site.register(Theme)
admin.site.register(AppConfigTag)
admin.site.register(JavaEnvironmentVariable)
admin.site.register(LanguageSqliteSequence)
admin.site.register(HotelServiceMapping)
admin.site.register(LocationCategory)
admin.site.register(StaticContent)
admin.site.register(UserHotel)


class AirlineDetailAdmin(admin.ModelAdmin):
    list_display = ('airlineName', 'airlineCode', 'imageName', 'position')
    search_fields = ('airlineName', 'airlineCode')


admin.site.register(AirlineDetail, AirlineDetailAdmin)


class AirportDetailAdmin(admin.ModelAdmin):
    list_display = ('airport_name', 'airport_code', 'country', 'city', 'city_code', 'location', 'status', 'position')
    search_fields = ('airport_name', 'airport_code', 'country', 'city', 'city_code')


admin.site.register(AirportDetail, AirportDetailAdmin)


class SettingsMetaAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'model_name', 'fields')


admin.site.register(SettingsMeta, SettingsMetaAdmin)


class SettingsImagesAdmin(admin.ModelAdmin):
    list_display = ('assetType', 'assetName', 'assetTimestamp')
    search_fields = ('assetName',)


admin.site.register(SettingsImages, SettingsImagesAdmin)


class HotelImagesAdmin(admin.ModelAdmin):
    list_display = ('assetType', 'assetName', 'assetTimestamp', 'hotel')
    search_fields = ('assetName', 'hotel__name')


admin.site.register(HotelImages, HotelImagesAdmin)


class UploadQueueAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'upload_type', 'state', 'error', 'created_on')
    search_fields = ('room_type__hotel__name', 'upload_type', 'state', 'error')


admin.site.register(UploadQueue, UploadQueueAdmin)


class JavaConfigAdmin(admin.ModelAdmin):
    list_display = ('related_hotel', 'module', 'config_key', 'config_val', 'val_type', 'description')
    search_fields = ('related_hotel__name', 'module', 'config_key', 'config_val')


admin.site.register(JavaConfig, JavaConfigAdmin)


class ColorStyleAdmin(admin.ModelAdmin):
    list_display = ('theme', 'color_style_name', 'attributes', 'lang_code')
    search_fields = ('theme__name', 'color_style_name', 'lang_code')


admin.site.register(ColorStyle, ColorStyleAdmin)


class ColorStyleMappingAdmin(admin.ModelAdmin):
    list_display = ('theme', 'color_style_name', 'apply_on', 'module_name')
    search_fields = ('theme__name', 'color_style_name', 'module_name')


admin.site.register(ColorStyleMapping, ColorStyleMappingAdmin)


class CommonSettingsAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'key', 'value')
    search_fields = ('key', '_value', 'room_type__hotel__name')


admin.site.register(CommonSettings, CommonSettingsAdmin)


class CurrencyTypesAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'currency_code', 'position', 'type', 'flag_image_name', 'locale_identifilre')
    search_fields = ('currency_name', 'currency_code', 'position', 'type')


admin.site.register(CurrencyTypes, CurrencyTypesAdmin)


class FeaturesSettingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'main_feature', 'feature_name', 'parameters')
    search_fields = ('room_type__hotel__name', 'feature_name', 'main_feature__name')


admin.site.register(FeaturesSetting, FeaturesSettingAdmin)


class FontStyleAdmin(admin.ModelAdmin):
    list_display = (
        'theme', 'font_name', 'font_size', 'font_color', 'shadow_color', 'shadow_offset', 'shadow_radius',
        'shadow_opacity',
        'attributes', 'lang_code')
    search_fields = ('theme__name', 'font_name', 'lang_code')


admin.site.register(FontStyle, FontStyleAdmin)


class FontStyleMappingAdmin(admin.ModelAdmin):
    list_display = ('theme', 'font_style_name', 'apply_on', 'module_name')
    search_fields = ('theme__name', 'font_style_name', 'module_name')


admin.site.register(FontStyleMapping, FontStyleMappingAdmin)


class HomeFeaturesAdmin(admin.ModelAdmin):
    list_display = ('enabled', 'name', 'room_type', 'image_name', 'selected_image_name', 'feature', 'position', 'command')
    search_fields = ('room_type__hotel__name', 'name')


admin.site.register(HomeFeatures, HomeFeaturesAdmin)


class ExportQueueAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'state', 'message', 'error', 'created_on', 'created_by')
    search_fields = ('room_type__hotel__name',)


admin.site.register(ExportQueue, ExportQueueAdmin)


class HotelServiceMappingInline(admin.TabularInline):
    model = HotelServiceMapping


class HotelServicesAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'name', 'feature_type', 'position', 'is_active')
    search_fields = ('room_type__hotel__name',)
    inlines = [
        HotelServiceMappingInline,
    ]


admin.site.register(HotelServices, HotelServicesAdmin)


class LocationSearchAdmin(admin.ModelAdmin):
    list_display = ('places', 'displayname', 'position', 'cat_id')


admin.site.register(LocationSearch, LocationSearchAdmin)


class SettingsImagesInline(admin.TabularInline):
    model = SettingsImages


class FeatureImageAdmin(admin.ModelAdmin):
    list_display = ('main_feature', 'icon_tag', 'room_type', 'hotel')
    inlines = [SettingsImagesInline, ]
    model = FeatureImages

    @staticmethod
    def main_feature(obj):
        return obj.main_feature.name

    @staticmethod
    def room_type(obj):
        return obj.main_feature.room_type.name

    @staticmethod
    def hotel(obj):
        return obj.main_feature.room_type.hotel.name


admin.site.register(FeatureImages, FeatureImageAdmin)


class FeatureImageAdminInline(admin.TabularInline):
    inlines = [SettingsImagesInline, ]
    model = FeatureImages


class MainFeaturesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'room_type', 'parent_id', 'enabled')
    search_fields = ('name', 'room_type__hotel__name')
    inlines = [FeatureImageAdminInline, ]


admin.site.register(MainFeatures, MainFeaturesAdmin)


class SplashImagesAdmin(admin.ModelAdmin):
    model = SplashImages


admin.site.register(SplashImages, SplashImagesAdmin)


class TimeZoneAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'city_name', 'country_name', 'timezone_id')
    search_fields = ('city_id', 'city_name', 'country_name', 'timezone_id')


admin.site.register(TimeZone, TimeZoneAdmin)


class WeathericonAdmin(admin.ModelAdmin):
    list_display = ('weathercode', 'unicode', 'iconvault_unicode', 'background_image')
    search_fields = ('weathercode', 'unicode', 'iconvault_unicode', 'background_image')


admin.site.register(Weathericon, WeathericonAdmin)


class DVLanguageAdmin(admin.ModelAdmin):
    search_fields = ('field', 'tag')
    list_display = ('tag', 'field', 'lang_code', 'module_name')


admin.site.register(DVLanguage, DVLanguageAdmin)


class DVHotelLanguageAdmin(admin.ModelAdmin):
    search_fields = ('field', 'tag', 'hotel__name')
    list_display = ('tag', 'field', 'lang_code', 'module_name', 'hotel')


admin.site.register(DVHotelLanguage, DVHotelLanguageAdmin)


class DVLanguageCodeAdmin(admin.ModelAdmin):
    list_display = ('lang_id', 'lang_code', 'display_name', 'position', 'is_active', 'image')


admin.site.register(DVLanguageCode, DVLanguageCodeAdmin)


class FQDNAdmin(admin.ModelAdmin):
    list_display = ('server', 'fqdn')


admin.site.register(FQDN, FQDNAdmin)


class DefaultImportSettingAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        if 'java_config_json' in request.FILES and DefaultImportSetting.objects.exists():
            new_data = json.loads(request.FILES['java_config_json'].read().decode('utf8'))
            old_data = json.loads(DefaultImportSetting.objects.get(pk=1).java_config_json.read().decode('utf8'))

            added = [data for data in new_data if data not in old_data]
            deleted = [data for data in old_data if data not in new_data]

            DefaultFileChanges.objects.create(created_by=request.user, added=added, deleted=deleted)

        if request.FILES:
            for name in request.FILES.values():
                if os.path.exists(MEDIA_ROOT + '/default_imports/' + str(name)):
                    os.remove(MEDIA_ROOT + '/default_imports/' + str(name))

        obj.save()


admin.site.register(DefaultImportSetting, DefaultImportSettingAdmin)


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            print(str(e))
            return super(PrettyJSONWidget, self).format_value(value)


class DefaultFileChangesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by',)
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


admin.site.register(DefaultFileChanges, DefaultFileChangesAdmin)


class DVHotelLanguageCodeAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'language_code', 'position', 'is_active')
    search_fields = ('hotel__name',)


admin.site.register(DVHotelLanguageCode, DVHotelLanguageCodeAdmin)


class HotelAirportDetailAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'airport', 'position', 'status')
    search_fields = ('hotel__name', 'airport__airport_name',)


admin.site.register(HotelAirportDetail, HotelAirportDetailAdmin)


class HomeServicesAdmin(admin.ModelAdmin):
    list_display = (
        'hotel', 'name', 'feature', 'type', 'image_name', 'selected_image_name', 'size', 'command', 'position',
        'enabled',
        'is_evening', 'is_morning')
    search_fields = ('hotel__name', 'name', 'feature')
    list_filter = ('hotel',)


admin.site.register(DVHomeService, HomeServicesAdmin)
