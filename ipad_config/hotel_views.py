# Python Imports
import json
import os
import shutil
import logging

# Django Imports
from django.http import FileResponse
from django.db import transaction
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse

# Project Imports
from .models import JavaConfig, Hotel, RoomType, MainFeatures, FeatureImages, SettingsImages, \
    CommonSettings, HomeFeatures, HotelServices, HotelServiceMapping, HotelImages, SplashImages, JavaConfigChanges, \
    DefaultImportSetting, DVHotelLanguage, DVHotelLanguageCode
from .forms import JavaConfigsForm, IPadProfileForm, MainFeaturesForm, FeaturesSettingForm, FeaturesImageForm, \
    CommonSettingForm, HomeFeatureForm, HotelServiceForm, HotelServiceMappingForm, SplashImageForm, SplashImageAddForm
from .middlewares import permission_required
from .import_views import upload_java_configs
from .utils import paginate, create_main_feature
from config.settings.base import MEDIA_ROOT

logger = logging.getLogger(__name__)


@permission_required("ipad_config.view_javaconfig")
def java_config_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    configs = hotel.java_configs.all()
    modules = configs.values('module').distinct()
    if request.method == "GET":
        try:
            module = request.GET['module']
            if module != '':
                configs = configs.filter(module=module)
        except Exception as e:
            logger.info(str(e))
            pass

        try:
            search_text = request.GET['search_text']
            if search_text:
                configs = configs.filter(
                    Q(config_key__icontains=search_text) |
                    Q(config_val__icontains=search_text)
                )
        except Exception as e:
            logger.info(str(e))
            pass

    configs = paginate(request, configs, 20)
    return render(request, 'pages/hotels/java_config/java_config_list.html',
                  {'configs': configs, 'hotel': hotel, 'modules': modules, 'changes_show': True}
                  )


@permission_required("ipad_config.can_bulk_unsync")
def unsync_java_configs(request, hotel_id):
    """
    @param hotel_id: database id of hotel
    @type request: object
    """
    hotel = Hotel.objects.get(pk=hotel_id)
    hotel.java_configs.all().update(is_synced=False)
    return redirect(reverse('java_configs_list', kwargs={'hotel_id': hotel.id}))


@permission_required("ipad_config.can_sync_from_default")
def sync_from_default(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    upload_java_configs(hotel, DefaultImportSetting.load().java_config_json.path, request=request)
    return redirect(reverse('java_configs_list', kwargs={'hotel_id': hotel.id}))


@permission_required("ipad_config.add_javaconfig")
def add_java_config(request, hotel_id, config_id=None):
    title = "Add Java Configuration"
    hotel = Hotel.objects.get(pk=hotel_id)
    config = None
    if config_id:
        title = "Edit Java Configuration"
        config = JavaConfig.objects.get(pk=config_id)

    if request.POST:
        if config:
            form = JavaConfigsForm(request.POST, instance=config)
        else:
            form = JavaConfigsForm(request.POST)
        if form.is_valid():
            config = form.save()
            JavaConfigChanges.objects.create(hotel=hotel, java_config=config, config_val=config.config_val,
                                             config_key=config.config_key, module=config.module, added_by=request.user)
            return redirect(reverse('java_configs_list', kwargs={'hotel_id': hotel.id}))
        else:
            return render(request, 'pages/hotels/java_config/java_configs_form.html',
                          {'form': form, 'title': title, 'hotel': hotel}
                          )
    else:
        form = JavaConfigsForm(initial={'related_hotel': hotel, 'hotel_id': hotel.id})
        if config:
            title = "Edit Java Configuration"
            form = JavaConfigsForm(instance=config)
        return render(request, 'pages/hotels/java_config/java_configs_form.html',
                      {'form': form, 'title': title, 'hotel': hotel, 'config': config}
                      )


@permission_required("ipad_config.view_javaconfig")
def show_import_changes(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    changes = JavaConfigChanges.objects.filter(hotel=hotel).order_by('-modified_on')
    changes = paginate(request, changes, 10)
    return render(request, 'pages/hotels/java_config/java_config_changes.html',
                  {'changes': changes, 'hotel': hotel}
                  )


@permission_required("ipad_config.view_roomtype")
def ipad_profiles(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profiles = hotel.room_types.all()
    return render(request, 'pages/hotels/ipad_profiles/ipad_profiles_list.html', {'profiles': profiles, 'hotel': hotel})


# Create Folder with json files
def create_folder(hotel_id, profile_id, dct):
    hotel_name = Hotel.objects.get(id=hotel_id).name.replace(" ", "_")
    os.mkdir('./{}'.format(hotel_name))
    path = './{}'.format(hotel_name)

    if 'main_feature' in dct:
        jsn = []

        features = list(RoomType.objects.get(id=profile_id).
                        main_features.values('id', 'parent_id', 'position', 'enabled', 'main_feature_id', 'name',
                                             'feature', 'sub_feature', 'room_id', 'controller_id',
                                             'contains_subcategory', 'app_version').order_by('id'))
        for feature in features:
            feature_images = {}
            for name in list(
                MainFeatures.objects.get(main_feature_id=feature['main_feature_id']).feature_icons.filter().values(
                    'icon_tag', 'setting_images__assetName')):
                if name['setting_images__assetName']:
                    feature_images[name["icon_tag"]] = name["setting_images__assetName"].split("/")[-1]

            for k, v in feature.items():
                if type(v) is int:
                    feature[k] = str(v)

            if feature['parent_id'] and int(feature['parent_id']) > 0:
                feature['parent_id'] = str(MainFeatures.objects.get(main_feature_id=int(feature['parent_id'])).id)
            elif feature['parent_id'] is None:
                feature['parent_id'] = "-1"

            feature['feature_images'] = str(feature_images).replace("'", "\"")
            feature.pop('main_feature_id')

            jsn.append(feature)
        with open(path + '/main_feature.json', 'w') as f:
            json.dump(jsn, f)

    if 'feature_setting' in dct:
        settings = list(RoomType.objects.get(id=profile_id).feature_settings.values('id', 'feature_id', 'feature_name',
                                                                                    'parameters'))
        for setting in settings:
            for k, v in setting.items():
                if type(v) is int:
                    setting[k] = str(v)
        with open(path + '/feature_setting.json', 'w') as f:
            json.dump(settings, f)

    if 'common_setting' in dct:
        settings = list(
            RoomType.objects.get(id=profile_id).common_settings.values('key', value=F('_value')))
        for setting in settings:
            setting['value'] = setting['value'].replace("'", "\"").replace("True", "true").replace("False",
                                                                                                   "false").replace(" ",
                                                                                                                    "")
        with open(path + '/common_setting.json', 'w') as f:
            json.dump(settings, f)

    if 'home_feature' in dct:
        feature = list(
            RoomType.objects.get(id=profile_id).home_features.values('id', 'enabled', 'name', 'image_name',
                                                                     'selected_image_name', 'feature', 'command',
                                                                     'position'))
        with open(path + '/home_feature.json', 'w') as f:
            json.dump(feature, f)

    if 'hotel_language_code' in dct:
        language_code = list(DVHotelLanguageCode.objects.filter(hotel=Hotel.objects.get(pk=hotel_id)).values(
            'position', 'is_active', lang_code=F('language_code__lang_code')))
        with open(path + '/hotel_language_code.json', 'w') as f:
            json.dump(language_code, f)

    if 'hotel_languages' in dct:
        language = list(DVHotelLanguage.objects.filter(hotel=Hotel.objects.get(pk=hotel_id)).values(
            'tag', 'field', 'lang_code', 'module_name'))
        with open(path + '/hotel_language.json', 'w') as f:
            json.dump(language, f)


# Export ipad data
@permission_required("ipad_config.view_roomtype")
def ipad_profile_export(request, hotel_id, profile_id):
    if dict(request.POST).get('tables'):

        # Create folder with json files of selected parameters
        create_folder(hotel_id, profile_id, dict(request.POST).get('tables'))
        logger.info("File Created")

        # get hotel name by which zip will be named
        hotel_name = Hotel.objects.get(id=hotel_id).name.replace(" ", "_")

        # make zip of above created folder
        shutil.make_archive('./{}'.format(hotel_name), 'zip', './', '{}'.format(hotel_name))
        logger.info("Zip created")

        # response for file to be downloaded
        response = FileResponse(open('./{}'.format(hotel_name + '.zip'), 'rb'), as_attachment=True)
        logger.info("Response Created")

        # remove zip and folder after download
        if os.path.exists('./{}'.format(hotel_name)):
            shutil.rmtree('./{}'.format(hotel_name))
        if os.path.exists('./{}.zip'.format(hotel_name)):
            os.remove('./{}.zip'.format(hotel_name))
        logger.info("Folder and zip removed from server")

        # send response
        return response

    hotel = Hotel.objects.get(id=hotel_id)
    profiles = hotel.room_types.all()
    return render(request, 'pages/hotels/ipad_profiles/ipad_profiles_list.html', {'profiles': profiles, 'hotel': hotel})


@permission_required("ipad_config.view_roomtype")
def export_java_config(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    configs = list(hotel.java_configs.values('module', 'config_key', 'config_val', 'val_type',
                                             'description', 'is_deletable', 'hotel_id', 'is_active',
                                             'delete_msg', 'is_deleted', 'created_by', 'created_on',
                                             'modified_by', 'modified_on', config_id=F('id')))

    # create json file
    with open('java_config.json', 'w') as f:
        json.dump(configs, f, default=str)

    # response for file to be downloaded
    response = FileResponse(open('java_config.json', 'rb'), as_attachment=True)
    logger.info("Response Created")

    # delete json file
    if os.path.exists('java_config.json'):
        os.remove('java_config.json')
    logger.info("Json File removed")

    return response


def ipad_profile_view(request, hotel_id, profile_id):
    profile = RoomType.objects.get(id=profile_id)
    hotel = Hotel.objects.get(id=hotel_id)
    return redirect(reverse('main_feature_settings_list', kwargs={'hotel_id': hotel.id, 'profile_id': profile.id}))


@permission_required("ipad_config.add_roomtype")
def add_ipad_profile(request, hotel_id):
    title = "Add iPad Profile"
    hotel = Hotel.objects.get(pk=hotel_id)
    form = IPadProfileForm(initial={'hotel': hotel})
    instance = RoomType(hotel=hotel)

    if request.POST:
        form = IPadProfileForm(request.POST, instance=instance)
        if form.is_valid():
            room_type = form.save()
            create_main_feature(room_type)
            return redirect(reverse('ipad_profiles_list', kwargs={'hotel_id': hotel.id}))
        else:
            return render(request, 'pages/hotels/ipad_profiles/ipad_profile_form.html',
                          {'form': form, 'title': title, 'hotel': hotel})

    return render(request, 'pages/hotels/ipad_profiles/ipad_profile_form.html',
                  {
                      'form': form, 'title': title, 'hotel': hotel
                  }
                  )


@permission_required("ipad_config.change_roomtype")
def edit_ipad_profile(request, hotel_id, profile_id):
    title = "Edit iPad Profile"
    hotel = Hotel.objects.get(pk=hotel_id)
    profile = RoomType.objects.get(pk=profile_id)
    room_type = RoomType.objects.get(pk=profile_id)
    form = IPadProfileForm(instance=room_type)

    if request.POST:
        form = IPadProfileForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            return redirect(reverse('ipad_profiles_list', kwargs={'hotel_id': hotel.id}))
        else:
            return render(request, 'pages/hotels/ipad_profiles/edit.html',
                          {
                              'form': form, 'title': title, 'hotel': hotel, 'profile': profile
                          }
                          )

    return render(request, 'pages/hotels/ipad_profiles/edit.html',
                  {
                      'form': form, 'title': title, 'hotel': hotel, 'profile': profile
                  }
                  )


def feature_settings_list(request, hotel_id, profile_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    feature_settings = profile.feature_settings.all()

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            feature_settings = feature_settings.filter(
                Q(feature_name__icontains=search_text) |
                Q(parameters__icontains=search_text)
            )
        except Exception as e:
            logger.info(str(e))
            pass

    feature_settings = paginate(request, feature_settings, 10)
    return render(request, 'pages/hotels/ipad_profiles/feature_settings_list.html',
                  {'feature_settings': feature_settings, 'profile': profile, 'hotel': hotel}
                  )


def common_settings_list(request, hotel_id, profile_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    common_settings = profile.common_settings.all()

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            common_settings = common_settings.filter(
                Q(key__icontains=search_text) |
                Q(_value__icontains=search_text)
            )
        except Exception as e:
            logger.info(str(e))
            pass

    form = CommonSettingForm(initial={'room_type': profile.id})

    return render(request, 'pages/hotels/ipad_profiles/common_settings_list.html',
                  {'common_settings': common_settings, 'profile': profile, 'hotel': hotel, 'form': form}
                  )


@permission_required("ipad_config.change_commonsettings")
def common_settings_edit(request, hotel_id, profile_id, setting_id=None):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    setting = CommonSettings.objects.none()
    form = CommonSettingForm()
    if setting_id:
        setting = CommonSettings.objects.get(pk=setting_id)
        form = CommonSettingForm(instance=setting, initial={'value': setting.value})

    if request.POST:
        if setting_id:
            form = CommonSettingForm(request.POST, instance=setting)
        else:
            form = CommonSettingForm(request.POST)

        if form.is_valid():
            obj = form.save()
            value = form.cleaned_data['value']
            try:
                value = json.loads(value)
            except Exception as e:
                logger.info(str(e))
                pass
            obj.value = value
            obj.save()
            return redirect(reverse('common_settings_list', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id}))
        else:
            return render(request, 'pages/hotels/ipad_profiles/common_settings_edit.html',
                          {
                              'form': form,
                              'setting': setting,
                              'profile': profile,
                              'hotel': hotel
                          }
                          )

    return render(request, 'pages/hotels/ipad_profiles/common_settings_edit.html',
                  {
                      'form': form,
                      'setting': setting,
                      'profile': profile,
                      'hotel': hotel
                  }
                  )


def home_feature_settings_list(request, hotel_id, profile_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    feature_settings = profile.home_features.all().order_by('position')
    form = HomeFeatureForm(initial={'room_type': profile.id})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            feature_settings = feature_settings.filter(
                Q(name__icontains=search_text) |
                Q(feature__icontains=search_text)
            )
        except Exception as e:
            logger.info(str(e))
            pass

    feature_settings = paginate(request, feature_settings, 10)
    return render(request, 'pages/hotels/ipad_profiles/home_feature_settings_list.html',
                  {'feature_settings': feature_settings, 'profile': profile, 'hotel': hotel, 'form': form}
                  )


@permission_required("ipad_config.change_homefeatures")
def home_feature_setting_edit(request, hotel_id, profile_id, setting_id=None):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    setting = HomeFeatures.objects.none()
    form = HomeFeatureForm()

    if setting_id:
        setting = HomeFeatures.objects.get(pk=setting_id)
        form = HomeFeatureForm(instance=setting)

    if request.POST:
        if setting_id:
            if request.FILES:
                if request.FILES.get("icon"):
                    if os.path.exists(MEDIA_ROOT + "/" + setting.room_type.theme.path() + "/setting_images/images/" +
                                      setting.image_name):
                        os.remove(MEDIA_ROOT + "/" + setting.room_type.theme.path() + "/setting_images/images/" +
                                  setting.image_name)
                if request.FILES.get("selected_icon"):
                    if os.path.exists(MEDIA_ROOT + "/" + setting.room_type.theme.path() + "/setting_images/images/" +
                                      setting.selected_image_name):
                        os.remove(MEDIA_ROOT + "/" + setting.room_type.theme.path() + "/setting_images/images/" +
                                  setting.selected_image_name)
            form = HomeFeatureForm(request.POST, request.FILES, instance=setting)
        else:
            form = HomeFeatureForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            if form.cleaned_data['icon']:
                asset = SettingsImages(assetType="image", assetName=request.FILES['icon'], theme=profile.theme)
                asset.save()
                name = asset.assetName.url.split("/")
                obj.image_name = name[len(name) - 1]
            if form.cleaned_data['selected_icon']:
                asset = SettingsImages(assetType="image", assetName=request.FILES['selected_icon'], theme=profile.theme)
                asset.save()
                name = asset.assetName.url.split("/")
                obj.selected_image_name = name[len(name) - 1]

            obj.id = obj.home_feature_id
            obj.save()
            return redirect(
                reverse('home_feature_settings_list', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id}))
        else:
            return render(request, 'pages/hotels/ipad_profiles/home_feature_setting_edit.html',
                          {
                              'form': form,
                              'setting': setting,
                              'profile': profile,
                              'hotel': hotel
                          }
                          )

    return render(request, 'pages/hotels/ipad_profiles/home_feature_setting_edit.html',
                  {
                      'form': form,
                      'setting': setting,
                      'profile': profile,
                      'hotel': hotel
                  }
                  )


@permission_required("ipad_config.change_mainfeatures")
def main_feature_settings_settings(request, hotel_id, profile_id, setting_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    feature = MainFeatures.objects.get(pk=setting_id)

    settings = None
    try:
        settings = feature.settings
    except Exception as e:
        logger.info(str(e))
        pass
    if settings:
        form = FeaturesSettingForm(instance=settings)
    else:
        form = FeaturesSettingForm(initial={'room_type': feature.room_type.id, 'main_feature': feature.main_feature_id,
                                            'feature_id': feature.main_feature_id})
    if request.POST:
        if settings:
            form = FeaturesSettingForm(request.POST, instance=settings)
        else:
            form = FeaturesSettingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(
                reverse('main_feature_settings_list', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id}))

    return render(request, 'pages/hotels/ipad_profiles/main_feature_settings.html',
                  {
                      'form': form,
                      'feature': feature,
                      'settings': settings,
                      'profile': profile,
                      'hotel': hotel
                  }
                  )


def main_feature_images(request, hotel_id, profile_id, setting_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    feature = MainFeatures.objects.get(pk=setting_id)

    images = None
    try:
        images = feature.feature_icons.all()
    except Exception as e:
        logger.info(str(e))
        pass

    form = FeaturesImageForm(initial={'main_feature': feature.main_feature_id})

    return render(request, 'pages/hotels/ipad_profiles/feature_image_list.html',
                  {
                      'form': form,
                      'feature': feature,
                      'feature_images': images,
                      'profile': profile,
                      'hotel': hotel
                  }
                  )


@permission_required("ipad_config.delete_mainfeatures")
def delete_main_feature_image(request, setting_id, image_id):
    feature = MainFeatures.objects.get(pk=setting_id)
    hotel_id = feature.room_type.hotel.id
    profile_id = feature.room_type.id
    try:
        feature_image = FeatureImages.objects.get(pk=image_id)
        SettingsImages.objects.filter(image=feature_image).delete()
        feature_image.delete()
    except Exception as e:
        logger.info(str(e))
    return redirect(reverse('main_feature_images', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id,
                                                           'setting_id': setting_id,
                                                           }))


@permission_required("ipad_config.change_mainfeatures")
def main_feature_image_edit(request, hotel_id, profile_id, setting_id, image_id=None):
    hotel = Hotel.objects.get(id=hotel_id)
    feature = MainFeatures.objects.get(pk=setting_id)
    profile = RoomType.objects.get(id=profile_id)
    images_list = os.listdir(MEDIA_ROOT + "/" + profile.theme.path() + "/setting_images/images")
    messages = []
    feature_image = FeatureImages.objects.none()
    form = FeaturesImageForm()
    if image_id:
        feature_image = FeatureImages.objects.get(pk=image_id)
        form = FeaturesImageForm(instance=feature_image)

    try:
        if request.POST:
            if image_id:
                form = FeaturesImageForm(request.POST, request.FILES, instance=feature_image)
            else:
                form = FeaturesImageForm(request.POST, request.FILES)
            if form.is_valid():
                with transaction.atomic():
                    feature_image = form.save()
                    try:
                        asset = feature_image.setting_images
                    except ObjectDoesNotExist:
                        asset = SettingsImages(assetType="image", image=feature_image)

                    if request.POST['image_name']:
                        image_name = profile.theme.path() + "/setting_images/images/" + request.POST['image_name']
                    else:
                        image_name = profile.theme.path() + "/setting_images/images/" + str(request.FILES['asset'].name)

                    if request.POST['image_name']:
                        asset.assetName = image_name
                    else:
                        if os.path.exists(MEDIA_ROOT + "/" + image_name):
                            os.remove(MEDIA_ROOT + "/" + image_name)
                        asset.assetName = request.FILES['asset']

                    asset.theme = profile.theme
                    asset.save()

                return redirect(reverse('main_feature_images', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id,
                                                                       'setting_id': setting_id,
                                                                       }))
            else:
                return redirect(reverse('main_feature_images', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id,
                                                                       'setting_id': setting_id}))

    except Exception as e:
        logger.info(str(e))
        messages.append({'tags': "error", 'message': "Please set asset"})

    return render(request, 'pages/hotels/ipad_profiles/feature_image_form.html',
                  {
                      'form': form,
                      'feature': feature,
                      'feature_image': feature_image,
                      'profile': profile,
                      'hotel': hotel,
                      'images_list': images_list,
                      'messages': messages
                  }
                  )


@permission_required("ipad_config.change_mainfeatures")
def main_feature_settings_edit(request, hotel_id, profile_id, setting_id=None):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    form = MainFeaturesForm(profile)
    feature = MainFeatures.objects.none()
    if setting_id:
        feature = MainFeatures.objects.get(pk=setting_id)
        form = MainFeaturesForm(profile, instance=feature)

    if request.POST:
        if setting_id:
            form = MainFeaturesForm(profile, request.POST, instance=feature)
        else:
            form = MainFeaturesForm(profile, request.POST)

        if form.is_valid():
            form.save()
            return redirect(
                reverse('main_feature_settings_list', kwargs={'hotel_id': hotel_id, 'profile_id': profile_id}))
        else:
            logger.info("false form validation failed")
            return render(request, 'pages/hotels/ipad_profiles/main_feature_edit.html',
                          {
                              'form': form,
                              'feature': feature,
                              'profile': profile,
                              'hotel': hotel
                          }
                          )

    return render(request, 'pages/hotels/ipad_profiles/main_feature_edit.html',
                  {
                      'form': form,
                      'feature': feature,
                      'profile': profile,
                      'hotel': hotel
                  }
                  )


def main_feature_settings_list(request, hotel_id, profile_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    main_features = profile.main_features.all().filter(enabled=True).order_by('position')
    disabled_main_features = profile.main_features.all().filter(enabled=False).order_by('position')

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            main_features = main_features.filter(
                Q(parent_id__name__icontains=search_text) |
                Q(feature__icontains=search_text) |
                Q(sub_feature__icontains=search_text) |
                Q(name__icontains=search_text)
            )

            disabled_main_features = disabled_main_features.filter(
                Q(parent_id__name__icontains=search_text) |
                Q(feature__icontains=search_text) |
                Q(sub_feature__icontains=search_text) |
                Q(name__icontains=search_text)
            )

            if request.GET['sort']:
                main_features = main_features.order_by(request.GET['sort'])
                disabled_main_features = disabled_main_features.order_by(request.GET['sort'])
        except Exception as e:
            logger.info(str(e))
            pass

    form = MainFeaturesForm(profile, initial={'room_type': profile.id})
    return render(request, 'pages/hotels/ipad_profiles/main_feature_list.html',
                  {'form': form,
                   'main_features': main_features,
                   'disabled_main_features': disabled_main_features,
                   'profile': profile, 'hotel': hotel
                   }
                  )


def profile_queue(request, hotel_id, profile_id):
    hotel = Hotel.objects.get(id=hotel_id)
    profile = RoomType.objects.get(id=profile_id)
    return render(request, 'pages/hotels/ipad_profiles/queue.html', {'profile': profile, 'hotel': hotel})


@permission_required("ipad_config.view_hotelservices")
def hotel_services_list(request, profile_id):
    profile = RoomType.objects.get(id=profile_id)
    hotel = Hotel.objects.get(id=profile.hotel.id)
    services = profile.hotel_services.all()
    form = HotelServiceForm(initial={'room_type': profile})

    return render(request, 'pages/hotels/ipad_profiles/hotel_services_list.html',
                  {'profile': profile, 'hotel': hotel, 'services': services, 'form': form})


@permission_required("ipad_config.change_hotelservices")
def hotel_services_edit(request, profile_id, service_id=None):
    # HotelServiceForm
    profile = RoomType.objects.get(pk=profile_id)
    hotel = profile.hotel
    hotel_service = HotelServices.objects.none()
    form = HotelServiceForm()
    if service_id:
        hotel_service = HotelServices.objects.get(pk=service_id)
        form = HotelServiceForm(instance=hotel_service)

    if request.POST:
        is_add_action_failed = False
        if service_id:

            if request.FILES:
                if os.path.exists(MEDIA_ROOT + "/" + hotel_service.icon.assetName.name):
                    os.remove(MEDIA_ROOT + "/" + hotel_service.icon.assetName.name)

            form = HotelServiceForm(request.POST, request.FILES, instance=hotel_service)
        else:
            is_add_action_failed = True
            form = HotelServiceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            if form.cleaned_data['service_icon']:
                asset = HotelImages(assetType="image", assetName=request.FILES['service_icon'], hotel=hotel)
                asset.save()
                obj.icon = asset
                obj.save()
            return redirect(reverse('hotel_services_list', kwargs={'profile_id': profile_id}))
        else:
            services = profile.hotel_services.all()
            template = 'pages/hotels/ipad_profiles/hotel_services_list.html' if \
                is_add_action_failed else 'pages/hotels/ipad_profiles/hotel_services_form.html '
            return render(request, template,
                          {
                              'form': form,
                              'hotel_service': hotel_service,
                              'services': services,
                              'profile': profile,
                              'hotel': hotel,
                              'is_form_failed': is_add_action_failed
                          }
                          )

    return render(request, 'pages/hotels/ipad_profiles/hotel_services_form.html',
                  {
                      'form': form,
                      'hotel_service': hotel_service,
                      'profile': profile,
                      'hotel': hotel
                  }
                  )


@permission_required("ipad_config.view_hotelservicemapping")
def hotel_services_mapping_list(request, service_id):
    hotel_service = HotelServices.objects.get(pk=service_id)
    profile = hotel_service.room_type
    hotel = Hotel.objects.get(id=profile.hotel.id)
    service_mappings = hotel_service.mappings.all()
    form = HotelServiceMappingForm(initial={'id': hotel_service, 'feature_type': hotel_service.feature_type})

    return render(request, 'pages/hotels/ipad_profiles/hotel_services_mapping_list.html',
                  {'profile': profile, 'hotel': hotel, 'hotel_service': hotel_service,
                   'service_mappings': service_mappings, 'form': form})


@permission_required("ipad_config.delete_hotelservicemapping")
def hotel_services_mapping_delete(request, hotel_service_id, mapping_id):
    hotel_service = HotelServices.objects.get(pk=hotel_service_id)
    HotelServiceMapping.objects.get(pk=mapping_id).delete()
    return redirect(reverse('hotel_services_mapping_list', kwargs={'service_id': hotel_service.id}))


@permission_required("ipad_config.change_hotelservicemapping")
def hotel_services_mapping_edit(request, hotel_service_id, mapping_id=None):
    # HotelServiceForm

    hotel_service = HotelServices.objects.get(pk=hotel_service_id)
    profile = hotel_service.room_type
    hotel = Hotel.objects.get(id=profile.hotel.id)
    mapping_obj = HotelServiceMapping.objects.none()
    form = HotelServiceMappingForm()
    if mapping_id:
        mapping_obj = HotelServiceMapping.objects.get(pk=mapping_id)
        form = HotelServiceMappingForm(instance=mapping_obj)

    if request.POST:
        is_add_action_failed = False
        if mapping_id:
            if request.FILES:
                if os.path.exists(MEDIA_ROOT + "/" + hotel_service.icon.assetName.name):
                    os.remove(MEDIA_ROOT + "/" + hotel_service.icon.assetName.name)

            form = HotelServiceMappingForm(request.POST, request.FILES, instance=mapping_obj)
        else:
            is_add_action_failed = True
            form = HotelServiceMappingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('hotel_services_mapping_list', kwargs={'service_id': hotel_service.id}))
        else:
            services = profile.hotel_services.all()
            template = 'pages/hotels/ipad_profiles/hotel_services_mapping_list.html' if\
                is_add_action_failed else 'pages/hotels/ipad_profiles/hotel_services_mapping_form.html'
            return render(request, template,
                          {
                              'form': form,
                              'hotel_service': hotel_service,
                              'services': services,
                              'profile': profile,
                              'hotel': hotel,
                              'mapping': mapping_obj,
                              'is_form_failed': is_add_action_failed
                          }
                          )

    return render(request, 'pages/hotels/ipad_profiles/hotel_services_mapping_form.html',
                  {
                      'form': form,
                      'hotel_service': hotel_service,
                      'profile': profile,
                      'hotel': hotel,
                      'mapping': mapping_obj
                  }
                  )


@permission_required("ipad_config.view_splashimages")
def splash_image_list(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    splash_images = hotel.splash_images.all()
    form = SplashImageAddForm(initial={'hotel': hotel})

    return render(request, 'pages/hotels/splash_image_list.html',
                  {'hotel': hotel, 'splash_images': splash_images, 'form': form})


@permission_required("ipad_config.delete_splashimages")
def splash_image_delete(request, hotel_id, image_id):
    hotel = Hotel.objects.get(id=hotel_id)
    splash_image = SplashImages.objects.get(pk=image_id)
    splash_image.icon.assetName.delete()
    splash_image.icon.delete()
    splash_image.delete()
    splash_images = hotel.splash_images.all()

    form = SplashImageAddForm(initial={'hotel': hotel})

    return render(request, 'pages/hotels/splash_image_list.html',
                  {'hotel': hotel, 'splash_images': splash_images, 'form': form})


@permission_required("ipad_config.change_splashimages")
def splash_image_edit(request, hotel_id, image_id=None):
    hotel = Hotel.objects.get(id=hotel_id)
    splash_image = SplashImages.objects.none()
    form = SplashImageForm()
    if image_id:
        splash_image = SplashImages.objects.get(pk=image_id)
        form = SplashImageForm(instance=splash_image)

    if request.POST:
        is_add_action_failed = False
        if image_id:

            if request.FILES:
                if os.path.exists(MEDIA_ROOT + "/" + splash_image.icon.assetName.name):
                    os.remove(MEDIA_ROOT + "/" + splash_image.icon.assetName.name)

            form = SplashImageForm(request.POST, request.FILES, instance=splash_image)
        else:
            is_add_action_failed = True
            form = SplashImageAddForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            if form.cleaned_data['splash_image']:
                asset = HotelImages(assetType="image", assetName=request.FILES['splash_image'], hotel=hotel)
                asset.save()
                obj.icon = asset
                obj.save()
            return redirect(reverse('splash_image_list', kwargs={'hotel_id': hotel_id}))
        else:
            splash_images = hotel.splash_images.all()
            template = 'pages/hotels/splash_image_list.html' if\
                is_add_action_failed else 'pages/hotels/splash_image_form.html'
            return render(request, template,
                          {
                              'form': form,
                              'splash_images': splash_images,
                              'splash_image': splash_image,
                              'hotel': hotel,
                              'is_form_failed': is_add_action_failed
                          }
                          )

    return render(request, 'pages/hotels/splash_image_form.html',
                  {
                      'form': form,
                      'splash_image': splash_image,
                      'hotel': hotel
                  }
                  )
