# Python Imports
import json

# Django Imports
from django.db import models
from config.settings.base import MEDIA_URL, ASSET_LOCATION, MEDIA_ROOT
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.fields import JSONField
from django.db.models import Q

# Project Imports
from setup.users.models import User
from .dgjava_tags import dgjava_dict

SERVERS = (
    ('DAS', 'DAS'),
    ('DVS', 'DVS'),
    ('HIS', 'HIS'),
    ('MDS', 'MDS'),
    ('VOD', 'VOD'),
    ('BUTLER', 'BUTLER'),
    ('ANALYTICS', 'ANALYTICS'),
)


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class DefaultImportSetting(SingletonModel):
    setting_assets = models.FileField(upload_to="default_imports")
    main_features = models.FileField(upload_to="default_imports")
    feature_settings = models.FileField(upload_to="default_imports")
    common_settings = models.FileField(upload_to="default_imports")
    home_feature_settings = models.FileField(upload_to="default_imports")
    theme_sqlite = models.FileField(upload_to="default_imports")
    java_config_json = models.FileField(upload_to="default_imports")
    # language_sqlite = models.FileField(upload_to="default_imports")


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    hotel_code = models.CharField(max_length=255)
    hotel_id = models.IntegerField()
    hotel_key = models.CharField(max_length=255, default="")

    def is_last_publish_success(self):
        room_types = RoomType.objects.filter(hotel=self)
        for room_type in room_types:
            last_queue = ExportQueue.objects.filter(room_type=room_type).first()
            if not last_queue.state == "SUCCESS":
                return False
        # it will reach here if all are success.
        return True

    def __str__(self):
        return self.name


class FQDN(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    server = models.CharField(max_length=30, choices=SERVERS)
    fqdn = models.CharField(max_length=255)

    def __str__(self):
        return self.server

    class Meta:
        unique_together = ['hotel', 'server']


def get_choices():
    obj = {}
    for key, value in dgjava_dict.items():
        obj[key] = key
    ls = (tupl for tupl in obj.items())
    return ls


class JavaEnvironmentVariable(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, choices=get_choices(), unique=True)
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key + " : " + self.value


class AppConfigTag(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, blank=True, default="")
    value = models.CharField(max_length=255, blank=True, default="")
    parent = models.ForeignKey('AppConfigTag', on_delete=models.CASCADE, related_name="child_tags", blank=True,
                               null=True, db_index=True)
    tag_type = models.CharField(max_length=50, default="text")

    def __str__(self):
        return self.key + " : " + self.tag_type


class SettingsMeta(models.Model):
    table_name = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=100)
    fields = models.TextField()

    def __str__(self):
        return self.table_name


"""
Seed Data Tables
"""


class AirlineDetail(models.Model):
    airlineName = models.CharField(max_length=255, db_index=True)
    airlineCode = models.CharField(max_length=255, db_index=True)
    imageName = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        db_table = 'airlinedetails'


class AirportDetail(models.Model):
    airport_name = models.CharField(max_length=255, db_index=True)
    airport_code = models.CharField(max_length=255, db_index=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    city_code = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    status = models.IntegerField()
    position = models.IntegerField()

    class Meta:
        db_table = 'airportdetails'

    def __str__(self):
        return self.airport_name


class TimeZone(models.Model):
    city_id = models.IntegerField(primary_key=True, db_index=True)
    city_name = models.CharField(max_length=255, blank=True, null=True)  # This field type is a guess.
    country_name = models.CharField(max_length=255, blank=True, null=True)  # This field type is a guess.
    timezone_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'time_zone'


class CurrencyTypes(models.Model):
    currency_name = models.CharField(max_length=255, primary_key=True, db_index=True)
    currency_code = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    flag_image_name = models.CharField(max_length=255, blank=True, null=True)
    locale_identifilre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'currency_types'


class Weathericon(models.Model):
    weathercode = models.IntegerField(primary_key=True, db_index=True)
    unicode = models.CharField(max_length=255, blank=True, null=True)
    iconvault_unicode = models.CharField(max_length=255, blank=True, null=True)
    background_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'weathericon'


"""
Seed Tables Ends
"""

"""
Theme Tables
"""


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def path(self):
        return self.name.replace(" ", "_")


# Theme Table
class ColorStyle(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="color_styles")
    color_style_name = models.CharField(max_length=255)
    attributes = models.TextField(blank=True, null=True)
    lang_code = models.CharField(max_length=255, default='en')

    # secondary_tabs_base_default

    class Meta:
        db_table = 'color_style'


# Theme Table
class ColorStyleMapping(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="color_style_mappings")
    color_style_name = models.CharField(max_length=255)
    apply_on = models.CharField(max_length=255)
    module_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'color_style_mapping'
        # unique_together = (('apply_on', 'module_name'),)


# Theme Table
class FontStyle(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="font_styles")
    font_style_name = models.CharField(max_length=255)
    font_name = models.CharField(max_length=255)
    font_size = models.FloatField(default='16')
    font_color = models.CharField(max_length=255)
    shadow_color = models.CharField(max_length=255)
    shadow_offset = models.CharField(max_length=255, default='{0,0}')
    shadow_radius = models.FloatField(default='0')
    shadow_opacity = models.FloatField(default='0')
    attributes = models.TextField(blank=True, null=True)
    lang_code = models.CharField(max_length=255, default='en')

    class Meta:
        db_table = 'font_style'


# Theme Table
class FontStyleMapping(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="font_style_mappings")
    font_style_name = models.CharField(max_length=255)
    apply_on = models.CharField(max_length=255)
    module_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'font_style_mapping'


"""
Theme Tables End
"""


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="room_types")
    name = models.CharField(max_length=100, default='default')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="room_type")

    class Meta:
        unique_together = ('name', 'hotel')

    def __str__(self):
        return self.hotel.name + " - " + self.name

    def get_name(self):
        return self.hotel.name + " : " + self.name


FILE_TYPE = (
    ('FILE', 'FILE'),
    ('ZIP', 'ZIP'),

)


def get_static_content_upload_path(instance, filename):
    path = str(instance.hotel.id)
    if instance.room_type:
        return path + "/" + instance.room_type.name + "/" + filename
    else:
        return path + "/" + filename


class StaticContent(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="static_content")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="static_content", null=True,
                                  blank=True)
    file_type = models.CharField(max_length=30, choices=FILE_TYPE,
                                 help_text="Suggested zip file structure: service_dir>zip")
    content = models.FileField(upload_to=get_static_content_upload_path,
                               help_text="Please re-upload file if roomtype selected or changed ")
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hotel.name + " | " + self.room_type.name + " | " + self.content.name.split("/")[-1] if \
            self.room_type else self.hotel.name + " | " + self.content.name.split("/")[-1]


class IpadBaseModel(models.Model):
    pass


def get_upload_path(instance, filename):
    theme = instance.theme.path()
    return theme + "/setting_images/images/" + filename


class SettingsImages(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="settings_images")
    assetType = models.CharField(max_length=255, default='image')
    _assetTimestamp = models.DateTimeField(auto_now_add=True)
    assetName = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    image = models.OneToOneField(IpadBaseModel, on_delete=models.CASCADE, related_name="setting_images", null=True,
                                 blank=True)

    @property
    def assetTimestamp(self):
        return self._assetTimestamp.timestamp()

    @property
    def get_absolute_image_url(self):
        return MEDIA_ROOT + "/" + self.assetName.name

    @property
    def filename(self):
        if self.assetName:
            name = self.assetName.name.split("/")
            name = name[len(name) - 1]
            return name
        return ""

    def __str__(self):
        return self.assetName.name

    class Meta:
        permissions = [
            ("bulk_delete_settingassets", "Can delete all settings assets"),
        ]


def get_hotel_images_upload_path(instance, filename):
    hotel_id = str(instance.hotel.id)
    return hotel_id + "/hotel_images/" + filename


class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_images")
    assetType = models.CharField(max_length=255, default='image')
    _assetTimestamp = models.DateTimeField(auto_now_add=True)
    assetName = models.FileField(upload_to=get_hotel_images_upload_path, null=True, blank=True)

    @property
    def assetTimestamp(self):
        return self._assetTimestamp.timestamp()

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(MEDIA_URL, self.assetName.url)

    def __str__(self):
        return self.assetName.name

    class Meta:
        permissions = [
            ("bulk_delete_hotelimages", "Can delete all hotel images"),
        ]


class CommonSettings(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="common_settings")
    key = models.CharField(max_length=255, blank=True, default="")
    _value = models.TextField(blank=True, default="", db_column="value")
    value_type = models.CharField(max_length=50, blank=True, default="")
    parent = models.ForeignKey('CommonSettings', on_delete=models.CASCADE, related_name="attributes", blank=True,
                               null=True)

    class Meta:
        db_table = 'common_settings'

    # @property
    # def value(self):
    #     obj=None
    #     if self.value_type == "list":
    #         obj=[]
    #         for attribute in self.attributes.all():
    #             data={}
    #             if len(attribute.key)>0:
    #                 data[attribute.key] = attribute.value
    #                 obj.append(data)
    #             else:
    #                 obj.append(attribute.value)
    #         pass
    #     elif self.value_type == "dict":
    #         obj={}
    #         for attribute in self.attributes.all():
    #             obj[attribute.key] = attribute.value
    #     elif self.value_type == "int":
    #         obj = int(self._value)
    #     elif self.value_type == "bool":
    #         obj = False if self._value == False else True
    #     else:
    #         fqdn_obj={}
    #         for f in FQDN.objects.all():
    #             fqdn_obj[f.server] = f.fqdn
    #         obj = self._value.format(**fqdn_obj)
    #     return obj

    @property
    def value(self):
        val = self._value
        for fqdn in FQDN.objects.filter(hotel=self.room_type.hotel):
            val = val.replace("{" + fqdn.server + "}", fqdn.fqdn)
        print(val)

        try:
            data = eval(val)
        except Exception as e:
            print(e)
            return val
        return data

    @value.setter
    def value(self, value):
        self._value = value


class FeaturesSetting(models.Model):
    feature_settings_id = models.AutoField(primary_key=True)
    id = models.IntegerField(default=0, blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="feature_settings")
    main_feature = models.OneToOneField('MainFeatures', models.CASCADE, unique=True, related_name='settings')
    feature_id = models.IntegerField(blank=True, default=0)
    feature_name = models.CharField(max_length=255)
    parameters = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'features_setting'


class HomeFeatures(models.Model):
    home_feature_id = models.AutoField(primary_key=True)
    id = models.IntegerField(default=0, blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="home_features")
    enabled = models.IntegerField(default=0, choices=((0, '0'), (1, '1')))
    name = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255)
    selected_image_name = models.CharField(max_length=255)
    feature = models.CharField(max_length=255)
    position = models.IntegerField(blank=True, null=True)
    command = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'home_features'


# class HotelEvents(models.Model):
#     room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="hotel_events")
#     title = models.TextField(primary_key=True)
#     description = models.TextField()
#     place = models.TextField()
#     event_date = models.TextField()
#     event_time = models.TextField()
#     event_type = models.TextField()
#     position = models.IntegerField()
#     visibility = models.IntegerField()

#     class Meta:
#         db_table = 'hotel_events'


# class HotelWidget(models.Model):
#     room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="hotel_widgets")
#     name = models.TextField(primary_key=True)
#     image = models.TextField()
#     description = models.TextField()
#     position = models.IntegerField()
#     visibility = models.IntegerField()

#     class Meta:
#         db_table = 'hotel_widget'


class MainFeatures(models.Model):
    main_feature_id = models.AutoField(primary_key=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="main_features", db_index=True)
    parent_id = models.ForeignKey('MainFeatures', on_delete=models.SET_DEFAULT, blank=True, related_name="children",
                                  default=0, null=True, db_constraint=False)
    position = models.IntegerField(blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    enabled = models.IntegerField(default=0, choices=((0, '0'), (1, '1')))
    name = models.CharField(max_length=255, blank=True, null=True)
    feature = models.CharField(max_length=255, blank=True, null=True)
    sub_feature = models.CharField(max_length=255, blank=True, null=True)
    room_id = models.IntegerField(blank=True, null=True, default=0)
    controller_id = models.IntegerField(blank=True, null=True, default=0)
    contains_subcategory = models.IntegerField(default=0, choices=((0, '0'), (1, '1')))
    app_version = models.CharField(max_length=255, blank=True, default=1)

    def __str__(self):
        return self.name

    @property
    def feature_images(self):
        obj = {}
        for icon in self.feature_icons.all():
            try:
                obj[icon.icon_tag] = icon.icon_name
            except Exception as e:
                print(e)
                raise
        return obj

    @feature_images.setter
    def feature_images(self, value):
        if len(value) > 0:
            value = json.loads(value) if type(value) is str else value
            for k, v in value.items():
                # print(k,v)
                try:
                    feature_image = FeatureImages(main_feature=self, icon_tag=k)
                    feature_image.save()
                    if len(v) > 0:
                        prefix = self.room_type.theme.path() + "/" + ASSET_LOCATION
                        try:
                            # settings_image = SettingsImages.objects.get(assetName=v,room_type=self.room_type)
                            settings_image = SettingsImages.objects.get(
                                Q(assetName=prefix + v),
                                Q(theme=self.room_type.theme),
                                Q(image__isnull=True),
                            )
                        except ObjectDoesNotExist:
                            settings_image = SettingsImages(assetName=prefix + v)
                            settings_image.theme = self.room_type.theme
                        settings_image.image = feature_image
                        settings_image.save()
                except Exception as e:
                    print(e)
                    # raise
        else:
            print(value)
        pass

    class Meta:
        db_table = 'main_features'
        ordering = ('position',)


class FeatureImages(IpadBaseModel):
    main_feature = models.ForeignKey(MainFeatures, related_name="feature_icons", on_delete=models.CASCADE)
    icon_tag = models.CharField(max_length=255, blank=True, default='')

    @property
    def icon_name(self):
        try:
            if self.setting_images:

                name = self.setting_images.assetName.name.split("/")
                name = name[len(name) - 1]
                return name

            else:
                return ""
        except Exception as e:
            print(e)
        return ""


class SplashImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="splash_images")
    image_key = models.CharField(max_length=255, blank=True, default="")
    position = models.IntegerField(default=1)
    visibility = models.IntegerField(default=1)
    icon = models.ForeignKey(HotelImages, on_delete=models.CASCADE, null=True)

    def get_image_key(self):
        if self.icon:
            name = self.icon.assetName.name.split("/")
            name = name[len(name) - 1]
            return name
        else:
            return ""

    def save(self, *args, **kwargs):
        try:
            self.image_key = self.get_image_key()
        except Exception as e:
            print(str(e))
            pass
        super(SplashImages, self).save(*args, **kwargs)

    class Meta:
        db_table = 'splash_images'


#
#               Location utlity tables
#
class LocationCategory(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, db_column='name')  # Field name made lowercase.
    position = models.IntegerField()

    class Meta:
        db_table = 'location_category'


class LocationSearch(models.Model):
    places = models.TextField(primary_key=True)
    displayname = models.TextField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    cat_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'location_search'


class HotelServices(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="hotel_services")
    name = models.CharField(max_length=255, blank=True, null=True)
    feature_type = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(default=1, choices=((0, '0'), (1, '1')))
    icon = models.ForeignKey(HotelImages, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'hotel_services'

    def __str__(self):
        return str(self.room_type) + " - " + self.name

    @property
    def image(self):
        try:
            if self.icon:

                name = self.icon.assetName.name.split("/")
                name = name[len(name) - 1]
                return name

            else:
                return ""
        except Exception as e:
            print(e)
        return ""


class HotelServiceMapping(models.Model):
    hotel_service_mapping = models.AutoField(primary_key=True)
    id = models.ForeignKey(HotelServices, on_delete=models.CASCADE, db_column="id", related_name="mappings",
                           verbose_name="Hotel Service")
    type_path = models.CharField(max_length=255)
    feature_type = models.CharField(max_length=255, blank=True, null=True)
    language_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'hotel_service_mapping'


class DVLanguage(models.Model):
    tag = models.TextField(blank=True, null=True)
    field = models.TextField(blank=True, null=True)
    lang_code = models.CharField(max_length=255, blank=True, null=True)
    module_name = models.CharField(max_length=255, blank=True, null=True, default='')

    class Meta:
        db_table = 'dv_language'
        ordering = ('lang_code', 'tag', 'field')


class DVHotelLanguage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="languages", on_delete=models.CASCADE, null=True)
    tag = models.TextField(blank=True, null=True)
    field = models.TextField(blank=True, null=True)
    lang_code = models.CharField(max_length=255, blank=True, null=True)
    module_name = models.CharField(max_length=255, blank=True, null=True, default='')

    class Meta:
        unique_together = ('hotel', 'tag', 'lang_code', 'module_name')
        ordering = ('lang_code', 'tag', 'field')


class DVLanguageCode(models.Model):
    lang_id = models.AutoField(primary_key=True, db_column='lang_id')
    lang_code = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(default=1)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'dv_language_code'

    def __str__(self):
        return self.display_name + "-" + self.lang_code


class LanguageSqliteSequence(models.Model):
    name = models.CharField(max_length=255, blank=True, default="")
    seq = models.IntegerField(default=0, blank=True)

    class Meta:
        db_table = 'sqlite_sequence'

    def __str__(self):
        return self.name


STATE = (
    ('PENDING', 'PENDING'),
    ('RUNNING', 'RUNNING'),
    ('SUCCESS', 'SUCCESS'),
    ('FAILED', 'FAILED'),
)

UPLOAD_TYPES = (
    ('THEME', 'THEME'),
    ('ASSET_ZIP', 'ASSET_ZIP'),
    ('LANGUAGE', 'LANGUAGE'),
    ('MAIN_FEATURES', 'MAIN_FEATURES'),
    ('COMMON_SETTINGS', 'COMMON_SETTINGS'),
    ('FEATURE_SETTINGS', 'FEATURE_SETTINGS'),
    ('HOME_FEATURE', 'HOME_FEATURE'),
    ('AIRPORT_DETAILS', 'AIRPORT_DETAILS'),
    ('AIRLINE_DETAILS', 'AIRLINE_DETAILS'),
)


class UploadQueue(models.Model):
    room_type = models.ForeignKey(RoomType, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name="upload_queue")
    file_path = models.CharField(default="", blank=True, max_length=255)
    upload_type = models.CharField(choices=UPLOAD_TYPES, max_length=100)
    state = models.CharField(choices=STATE, max_length=50)
    theme_id = models.IntegerField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_on',)

    def __str__(self):
        return self.upload_type + " : " + self.state


class ExportQueue(models.Model):
    room_type = models.ForeignKey(RoomType, blank=True, null=True, on_delete=models.CASCADE,
                                  related_name='publish_queue')
    state = models.CharField(choices=STATE, max_length=50)
    message = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=255, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.room_type.name + " : " + self.state


# #
# #               Radio utlity tables
# #
# class VtunerCountry(models.Model):
#     room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="vtuner_countries")
#     country_id = models.IntegerField(blank=True, null=True)
#     name = models.TextField(blank=True, null=True)
#     type = models.TextField(blank=True, null=True)
#     position = models.IntegerField(blank=True, null=True)
#     visibility = models.IntegerField(blank=True, null=True)

#     # class Meta:
#     #     db_table = 'vtuner_country'


# class VtunerLanguage(models.Model):
#     room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="vtuner_languages")
#     lang_id = models.TextField()
#     name = models.TextField()
#     type = models.TextField()
#     position = models.IntegerField()
#     visibility = models.IntegerField()

#     # class Meta:
#     #     db_table = 'vtuner_language'


# class VtunerMainCategory(models.Model):
#     room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="vtuner_main_categories")
#     name = models.TextField(blank=True, null=True)
#     type = models.TextField(blank=True, null=True)
#     position = models.IntegerField(blank=True, null=True)
#     visibility = models.IntegerField(blank=True, null=True)

#     # class Meta:
#     #     db_table = 'vtuner_main_category'


class JavaConfig(models.Model):
    VALUE_TYPES = (
        ('common', 'common'),
        ('environment', 'environment'),
        ('environment_substring', 'environment_substring')
    )
    # config_id = models.IntegerField()
    related_hotel = models.ForeignKey(Hotel, related_name="java_configs", on_delete=models.CASCADE,
                                      db_column="related_hotel")
    module = models.CharField(max_length=50)
    config_key = models.CharField(max_length=100)
    config_val = models.TextField()
    val_type = models.CharField(max_length=50, default="text", choices=VALUE_TYPES)
    description = models.TextField()
    is_deletable = models.BooleanField(default=False)
    hotel_id = models.IntegerField()
    is_active = models.BooleanField(default=True)
    delete_msg = models.CharField(default="", blank=True, max_length=255)
    is_deleted = models.BooleanField(default=True)
    created_by = models.IntegerField(default=1, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField(default=1, blank=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_synced = models.BooleanField(default=False)

    def __str__(self):
        return self.module + ": " + self.config_key

    class Meta:
        permissions = [
            ("can_bulk_unsync", "Can change the status of javaconfig to unsync"),
        ]

    def get_config_val(self):
        val = self.config_val
        try:
            if 'http' in val:
                for fqdn in FQDN.objects.filter(hotel=self.related_hotel):
                    val = val.replace("{" + fqdn.server + "}", fqdn.fqdn)
            elif "HOTEL_CODE" in val:
                val = val.replace("{HOTEL_CODE}", self.related_hotel.hotel_code)
                return val

            elif "HOTEL_ID" in val:
                val = val.replace("{HOTEL_ID}", str(self.related_hotel.hotel_id))
                return val
        except Exception as e:
            print(e)
            raise
        return val


class HotelBookmark(models.Model):
    user = models.ForeignKey(User, related_name='bookmarked_hotels', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='bookmarks', on_delete=models.CASCADE)


class UserHotel(models.Model):
    user = models.ForeignKey(User, related_name='user_hotels', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.hotel.name


class HotelAirportDetail(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_airport_details")
    airport = models.ForeignKey(AirportDetail, on_delete=models.CASCADE)
    status = models.IntegerField()
    position = models.IntegerField()

    class Meta:
        unique_together = ('hotel', 'airport')

    def __str__(self):
        return self.airport.airport_name


class DVHotelLanguageCode(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_langauge_codes")
    language_code = models.ForeignKey(DVLanguageCode, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, blank=True, default=0)
    is_active = models.IntegerField(default=1)

    class Meta:
        unique_together = ('hotel', 'language_code')

    def __str__(self):
        return self.language_code.lang_code


class DVHomeService(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="home_services", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255, default='')
    selected_image_name = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='with_image')
    feature = models.CharField(max_length=255, default='with_image')
    size = models.CharField(max_length=255)
    command = models.CharField(max_length=255, default='with_image')
    position = models.IntegerField(default=1)
    enabled = models.IntegerField(default=1, choices=((0, '0'), (1, '1')))
    is_evening = models.IntegerField(blank=True, null=True)
    is_morning = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('hotel', 'name')

    def __str__(self):
        return self.name


# CREATE TABLE "home_services" (
#   "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#   "name" text NOT NULL,
#   "image_name" text NOT NULL,
#   "selected_image_name" text NOT NULL,
#   "type" text NOT NULL,
#   "feature" text NOT NULL,
#   "size" text NOT NULL,
#   "command" text NULL,
#   "position" integer NOT NULL,
#   "enabled" integer NOT NULL
# , "is_evening" integer NULL, "is_morning" integer NULL)

class JavaConfigChanges(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    java_config = models.ForeignKey(JavaConfig, on_delete=models.CASCADE)
    module = models.CharField(max_length=50, null=True)
    config_val = models.TextField(null=True)
    config_key = models.CharField(max_length=100, null=True)
    added_by = models.CharField(max_length=100)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hotel.name + " | " + self.module + " | " + self.config_key


class FilterFromResultQuerySet(models.QuerySet):

    def settings_table_added(self):
        return self.filter(type='settings', table=None, action='added')

    def settings_table_deleted(self):
        return self.filter(type='settings', table=None, action='deleted')

    def language_table_added(self):
        return self.filter(type='language', table=None, action='added')

    def language_table_deleted(self):
        return self.filter(type='language', table=None, action='deleted')

    def settings_table_altered(self):
        dct = {}
        for data in self.filter(type="settings", table__isnull=False):
            dct[data.table] = dct.get(data.table, [])
            dct[data.table].append(data)
        return dct

    def language_table_altered(self):
        dct = {}
        for data in self.filter(type="language", table__isnull=False):
            dct[data.table] = dct.get(data.table, [])
            dct[data.table].append(data)
        return dct

    def image(self):
        return self.filter(type='image')


class IpadConfigChanges(models.Model):
    ACTION = (
        ("added", "added"),
        ("deleted", "deleted"),
    )

    TYPE = (
        ("settings", "settings"),
        ("language", "language"),
        ("image", "image")
    )

    queue = models.ForeignKey(ExportQueue, on_delete=models.CASCADE, related_name="changes_queue")
    action = models.CharField(max_length=50, choices=ACTION)
    type = models.CharField(max_length=50, choices=TYPE)
    name = models.TextField()
    table = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    objects = FilterFromResultQuerySet.as_manager()

    class Meta:
        db_table = "ipad_config_changes"


class DefaultFileChanges(models.Model):
    class Meta:
        db_table = "default_file_changes"

    created_by = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now=True)
    deleted = JSONField()
    added = JSONField()

    def __str__(self):
        return self.created_by + " | " + str(self.created_on)
