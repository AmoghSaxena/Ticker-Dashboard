"""
Created on 28-Dec-2019

@author: sumit-rathore
"""

from django import forms
from django.forms import ModelForm
from .models import Theme, FontStyle, FontStyleMapping, ColorStyle, ColorStyleMapping, \
    AirlineDetail, JavaConfig, RoomType, MainFeatures, FeaturesSetting, FeatureImages, \
    CommonSettings, HomeFeatures, DVHotelLanguage, HotelImages, StaticContent, HotelServices, HotelServiceMapping, \
    SplashImages, DVHotelLanguageCode, HotelAirportDetail, DVLanguageCode, DVLanguage, AirportDetail, SettingsImages


class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = '__all__'


class SettingsImagesForm(ModelForm):
    class Meta:
        model = SettingsImages
        fields = '__all__'
        exclude = ('image',)
        widgets = {'theme': forms.HiddenInput()}


class FormStyleForm(ModelForm):
    class Meta:
        model = FontStyle
        fields = '__all__'


class FontStyleMappingForm(ModelForm):
    class Meta:
        model = FontStyleMapping
        fields = '__all__'


class ColorStyleForm(ModelForm):
    class Meta:
        model = ColorStyle
        fields = '__all__'


class ColorStyleMappingForm(ModelForm):
    class Meta:
        model = ColorStyleMapping
        fields = '__all__'


class AirlineDetailForm(ModelForm):
    class Meta:
        model = AirlineDetail
        fields = '__all__'


class AirportDetailForm(ModelForm):
    class Meta:
        model = AirportDetail
        fields = '__all__'


class JavaConfigsForm(ModelForm):
    class Meta:
        model = JavaConfig
        fields = '__all__'
        exclude = ('created_by', 'modified_by')
        widgets = {'related_hotel': forms.HiddenInput(), 'hotel_id': forms.HiddenInput()}


class IPadProfileForm(ModelForm):
    class Meta:
        model = RoomType
        fields = ('name', 'theme', 'hotel')
        widgets = {'hotel': forms.HiddenInput()}


class MainFeaturesForm(ModelForm):
    parent_id = forms.ModelChoiceField(queryset=None, label='Parent', required=False, initial=0)

    def __init__(self, profile, *args, **kwargs):
        parents = MainFeatures.objects.filter(room_type=profile)
        super(MainFeaturesForm, self).__init__(*args, **kwargs)
        self.fields['parent_id'].queryset = parents

    class Meta:
        model = MainFeatures
        fields = (
            'room_type', 'name', 'feature', 'parent_id', 'position', 'enabled', 'sub_feature', 'contains_subcategory')
        widgets = {'room_type': forms.HiddenInput(), 'enabled': forms.RadioSelect(),
                   'contains_subcategory': forms.RadioSelect()}


class FeaturesSettingForm(ModelForm):
    class Meta:
        model = FeaturesSetting
        fields = ('room_type', 'feature_name', 'parameters', 'main_feature', 'feature_id')
        widgets = {'room_type': forms.HiddenInput(), 'main_feature': forms.HiddenInput(),
                   'feature_id': forms.HiddenInput()}


class FeaturesImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon_tag'].required = True
    asset = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = FeatureImages
        fields = ('main_feature', 'icon_tag')
        widgets = {'main_feature': forms.HiddenInput()}


# class RoomTypeThemeMappingForm(ModelForm):
#     class Meta:
#         model = RoomTypeThemeMapping
#         fields = '__all__'


class CommonSettingForm(ModelForm):
    value = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 20}))

    class Meta:
        model = CommonSettings
        fields = ('room_type', 'key', 'value')
        widgets = {'room_type': forms.HiddenInput(), 'value': forms.Textarea()}


class HotelLanguageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(HotelLanguageForm, self).__init__(*args, **kwargs)
        self.fields['tag'].strip = False
        self.fields['field'].strip = False

    class Meta:
        model = DVHotelLanguage
        fields = ('hotel', 'tag', 'field', 'lang_code', 'module_name')
        widgets = {'hotel': forms.HiddenInput()}


class HomeFeatureForm(ModelForm):
    icon = forms.ImageField(widget=forms.FileInput(), required=False)
    selected_icon = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = HomeFeatures
        fields = ('room_type', 'name', 'feature', 'command', 'enabled', 'position')
        widgets = {'room_type': forms.HiddenInput(), 'enabled': forms.RadioSelect()}


class HotelImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assetName'].required = True

    class Meta:
        model = HotelImages
        fields = ('hotel', 'assetType', 'assetName')
        widgets = {'hotel': forms.HiddenInput()}


class HotelStaticContentForm(ModelForm):
    # def __init__(self, hotelid, *args, **kwargs):
    #     super(HotelStaticContentForm, self).__init__(*args, **kwargs)
    #     self.fields['room_type'] = forms.ModelChoiceField(
    #         queryset=RoomType.objects.filter(hotel=hotelid),required=False
    #     )

    class Meta:
        model = StaticContent
        fields = ('hotel', 'room_type', 'file_type', 'content')
        widgets = {'hotel': forms.HiddenInput()}


class HotelServiceForm(ModelForm):
    service_icon = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = HotelServices
        fields = ('room_type', 'name', 'feature_type', 'position', 'service_icon', 'is_active')
        widgets = {'room_type': forms.HiddenInput(), 'is_active': forms.RadioSelect()}


class HotelServiceMappingForm(ModelForm):
    class Meta:
        model = HotelServiceMapping
        fields = ('id', 'type_path', 'feature_type', 'language_code')
        widgets = {'id': forms.HiddenInput()}


class SplashImageForm(ModelForm):
    splash_image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = SplashImages
        fields = ('hotel', 'position', 'visibility', 'splash_image')
        widgets = {'hotel': forms.HiddenInput()}


class SplashImageAddForm(ModelForm):
    splash_image = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = SplashImages
        fields = ('hotel', 'position', 'visibility', 'splash_image')
        widgets = {'hotel': forms.HiddenInput()}


class HotelAirportDetailForm(ModelForm):
    class Meta:
        model = HotelAirportDetail
        fields = ('hotel', 'airport', 'position', 'status')
        widgets = {'hotel': forms.HiddenInput()}


class HotelLanguageCodeForm(ModelForm):
    class Meta:
        model = DVHotelLanguageCode
        fields = ('hotel', 'language_code', 'position', 'is_active')
        widgets = {'hotel': forms.HiddenInput()}


class DVLanguageCodeForm(ModelForm):
    class Meta:
        model = DVLanguageCode
        fields = ('lang_code', 'display_name', 'image', 'position', 'is_active')


class DVLanguageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DVLanguageForm, self).__init__(*args, **kwargs)
        self.fields['tag'].strip = False
        self.fields['field'].strip = False

    class Meta:
        model = DVLanguage
        fields = ('tag', 'field', 'lang_code', 'module_name')
