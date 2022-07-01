# Python Imports
import requests
import sqlite3
import tempfile
import os
import zipfile
import logging

# Django Imports
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Prefetch
from django.contrib import messages
from django.db import transaction, OperationalError
from django.apps import apps
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.static import serve

# Restframework Imports
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Project Imports
from .models import *
from .dvp_client import CloudClient
from .serializers import MainFeatureSerializer, MainFeatureUpdateSerializer
from config.settings.base import MEDIA_ROOT
from .import_views import upload_java_configs
from .middlewares import permission_required
from .forms import HotelLanguageForm, HotelImageForm, HotelStaticContentForm, HotelAirportDetailForm, \
    HotelLanguageCodeForm, DVLanguageForm, DVLanguageCodeForm
from config.celery_app import app
from .publish_ipad_conf import export_sqlite, export_assest_json, export_language_sqlite
from .utils import create_main_feature, paginate

logger = logging.getLogger(__name__)


class MediaContent(APIView):

    @staticmethod
    def get(request):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        file_path = "test"
        print(file_path)
        return serve(request, file_path, MEDIA_ROOT, True)


@api_view()
def media_content(request, file_path):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print(file_path)
    return serve(request, file_path, MEDIA_ROOT, True)


class MainFeatureList(ListAPIView):
    serializer_class = MainFeatureSerializer

    def get_queryset(self):
        profile_id = self.kwargs['profile']
        profile = RoomType.objects.get(pk=profile_id)
        # return MainFeatures.objects.filter(parent_id=None,room_type=profile).prefetch_related('children')
        return MainFeatures.objects.filter(parent_id=None, room_type=profile).prefetch_related(Prefetch('children'))


class MainFeatureUpdate(RetrieveUpdateAPIView):
    queryset = MainFeatures.objects.all()
    serializer_class = MainFeatureUpdateSerializer


@permission_required("ipad_config.change_roomtype")
def config_profile(request, profile_id):
    # themes = Theme.objects.all()
    profile = RoomType.objects.get(pk=profile_id)
    return render(request, 'pages/profiles/profile_edit.html',
                  {'profile': profile})


@permission_required("")
def dv5_head_response(request):
    return HttpResponse("Ok")


@permission_required("ipad_config.change_roomtype")
def edit_profile(request, profile_id):
    # themes = Theme.objects.all()
    profile = RoomType.objects.get(pk=profile_id)

    if request.method == "POST":
        name = request.POST["name"]
        profile.name = name
        profile.save()

    return render(request, 'pages/profiles/profile_edit.html',
                  {'profile': profile})


@permission_required("")
def assets_json(request, profile):
    profile = RoomType.objects.get(name=profile)
    ipad = []
    settings_images = profile.settings_images.all()  # .values('assetType','assetName')
    for s in settings_images:
        obj = {'assetType': s.assetType, 'assetTimestamp': str(int(s.assetTimestamp))}
        url = s.assetName.url
        url = url.replace("%20", " ")
        obj['assetName'] = request.scheme + "://" + request.get_host() + url
        ipad.append(obj)
    # test = model_to_dict(settings_images)
    # print(test)
    print(ipad)
    return JsonResponse({"ipad": ipad})


@permission_required("")
def feature_ordering(request, profile_id):
    profile = RoomType.objects.get(pk=profile_id)
    return render(request, 'pages/hotels/feature_ordering.html', {'profile': profile})


@permission_required("")
def splash_images(request, profile_id):
    profile = RoomType.objects.get(pk=profile_id)
    return render(request, 'pages/splash_image.html', {'profile': profile})


@permission_required("ipad_config.change_mainfeatures")
def select_features(request):
    if request.method == "POST":
        profile_id = request.POST["profile_id"]
        profile = RoomType.objects.get(pk=profile_id)
        features = request.POST.getlist('feature')

        # Disabled all of them before enabling selected.
        for f in MainFeatures.objects.filter(room_type=profile):
            f.enabled = False
            f.save()

        for feature in features:
            try:
                main_feature = MainFeatures.objects.get(room_type=profile, name=feature)
                main_feature.enabled = True
                main_feature.save()
            except ObjectDoesNotExist:
                print("Creating New .... {0}".format(feature.name))
                main_feature = MainFeatures(room_type=profile, name=feature, enabled=True)
                main_feature.save()

    return redirect('feature_ordering')


@permission_required("ipad_config.add_roomtype")
def add_profile(request):
    # themes = Theme.objects.all()
    profiles = RoomType.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        # theme = Theme.objects.get(pk=request.POST["theme"])
        room_type = RoomType(name=name)
        room_type.save()

        create_main_feature(room_type)

    return render(request, 'pages/profiles/profile.html', {'profiles': profiles})


@permission_required("")
def confirm_delete_profile(request, profile_id):
    return render(request, 'pages/confirm_delete_profile.html', {})


@permission_required("")
def delete_profile(request, profile_id):
    profile = RoomType.objects.get(pk=profile_id)
    return render(request, 'pages/profiles/profile.html', {"profiles": profile})


@permission_required("")
def home(request):
    profiles = RoomType.objects.all()
    # themes = Theme.objects.all()
    return render(request, 'pages/trash/home.html', {'profiles': profiles})


@app.task
def export_ipad_configuration_task():
    print("checking ")
    if ExportQueue.objects.filter(state="RUNNING").exists():
        print("Already running ")

    else:
        print("checking for pending jobs ")
        for queue in ExportQueue.objects.filter(state="PENDING")[:1]:
            print("got pending jobs ")
            queue.state = "RUNNING"
            queue.save()
            try:
                profile = queue.room_type
                path = MEDIA_ROOT + "/" + str(profile.hotel.id) + "/" + profile.name
                if profile.name == 'default':
                    path = MEDIA_ROOT + "/" + str(profile.hotel.id)
                if not os.path.exists(path):
                    os.makedirs(path)
                try:
                    export_sqlite(path, profile, queue)
                    export_language_sqlite(path, profile, queue)
                    path = path + "/" + "setting_images"
                    if not os.path.exists(path):
                        os.makedirs(path)
                    export_assest_json(path, profile, queue)
                    queue.state = "SUCCESS"
                except Exception as e:
                    print(e)
                    queue.state = "FAILED"
                    queue.error = str(e)
            except Exception as e:
                print(e)
                queue.error = str(e)
                queue.state = "FAILED"
            queue.save()


@permission_required("ipad_config.change_mainfeatures")
def export_ipad_configuration(request, profile_id):
    profile = RoomType.objects.get(pk=profile_id)

    if request.POST:
        queue = ExportQueue()
        queue.created_by = request.user
        queue.room_type = profile
        queue.state = "PENDING"
        queue.message = request.POST['publish_message']
        queue.save()
        profile = queue.room_type
        export_ipad_configuration_task.delay()
        return redirect(reverse('publish_queue', kwargs={'hotel_id': profile.hotel.id}))

    # Confirm Publish
    return render(request, 'pages/hotels/ipad_profiles/confirm_publish.html',
                  {'profile': profile, 'hotel': profile.hotel}
                  )


@permission_required("")
def publish_queue(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    queue = hotel.room_types.none()
    profiles = hotel.room_types.all()
    for profile in profiles:
        queue |= profile.publish_queue.all()

    return render(request, 'pages/hotels/publish_list.html',
                  {'queue': queue.order_by("-created_on"), 'hotel': hotel}
                  )


@permission_required("")
def show_publish_changes(request, **kwargs):
    queue = ExportQueue.objects.get(pk=kwargs["queue_id"])
    changes = IpadConfigChanges.objects.filter(queue=queue)
    hotel = Hotel.objects.get(id=kwargs["hotel_id"])

    return render(request, 'pages/hotels/publish_changes.html',
                  {'queue': changes, 'hotel': hotel}
                  )


def import_main_feature_task(file_path, profile):
    json_data = open(file_path, 'r')
    data1 = json.load(json_data)  # deserializes it
    if len(data1) > 0:
        MainFeatures.objects.filter(room_type=profile).delete()
        data1 = sorted(data1, key=lambda k: k['parent_id'])
        for obj_data in data1:
            with transaction.atomic():
                # obj_data['parent_id'] = None
                f = obj_data.pop('feature_images')
                parent_id = int(obj_data.pop('parent_id'))
                m = MainFeatures(**obj_data)
                m.room_type = profile
                if parent_id > 0:
                    try:
                        parent = MainFeatures.objects.get(room_type=profile, id=parent_id)
                        m.parent_id = parent
                    except ObjectDoesNotExist as e:
                        print(e, parent_id)
                elif parent_id < 0:
                    m.parent_id = None
                m.save()
                m.feature_images = f
                m.save()


@permission_required("ipad_config.change_mainfeatures")
def import_main_features(request):
    if request.method == 'POST' and request.FILES['main_features_json']:
        profile_type = request.POST['profile_type']
        profile = RoomType.objects.get(pk=profile_type)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["main_features_json"].chunks():
                f.write(chunk)

            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "MAIN_FEATURES"
            queue.state = "PENDING"
            queue.room_type = profile
            queue.save()
            upload_task.delay()

        return redirect(
            reverse('main_feature_settings_list', kwargs={'hotel_id': profile.hotel.id, 'profile_id': profile.id}))
    return HttpResponse("Method not supported")


def import_common_settings_task(file_path, profile):
    json_data = open(file_path, 'r')
    print(json_data)
    data1 = json.load(json_data)  # deserializes it

    if len(data1) > 0:
        CommonSettings.objects.filter(room_type=profile).delete()
        for obj_data in data1:
            # print(obj_data)
            print("Inner.. %s" % obj_data)
            value = obj_data.pop("value")
            value = json.loads(value) if type(value) is str else value
            m = CommonSettings(**obj_data)
            m.room_type = profile
            m.save()
            m.value = value
            m.save()


@permission_required("")
def import_common_settings(request):
    if request.method == 'POST' and request.FILES['common_settings_json']:
        profile_type = request.POST['profile_type']
        profile = RoomType.objects.get(pk=profile_type)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["common_settings_json"].chunks():
                f.write(chunk)

            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "COMMON_SETTINGS"
            queue.state = "PENDING"
            queue.room_type = profile
            queue.save()
            upload_task.delay()
        return redirect(
            reverse('common_settings_list', kwargs={'hotel_id': profile.hotel.id, 'profile_id': profile.id}))
    return HttpResponse("Method not supported")


def import_feature_settings_task(file_path, profile):
    json_data = open(file_path, 'r')
    data1 = json.load(json_data)  # deserialises it
    insert_list = []
    if len(data1) > 0:
        FeaturesSetting.objects.filter(room_type=profile).delete()
        for obj_data in data1:
            print("Inner.. %s" % obj_data)
            feature = MainFeatures.objects.get(id=obj_data['feature_id'], room_type=profile)
            obj_data.pop('feature_id')
            m = FeaturesSetting(**obj_data)
            m.feature_id = feature.id
            m.main_feature_id = feature.main_feature_id
            m.room_type = profile
            insert_list.append(m)
        FeaturesSetting.objects.bulk_create(insert_list)  # Success in performance


@permission_required("ipad_config.change_featuresetting")
def import_features_setting(request):
    if request.method == 'POST' and request.FILES['features_setting_json']:
        profile_type = request.POST['profile_type']
        profile = RoomType.objects.get(pk=profile_type)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["features_setting_json"].chunks():
                f.write(chunk)

            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "FEATURE_SETTINGS"
            queue.state = "PENDING"
            queue.room_type = profile
            queue.save()
            upload_task.delay()

        return redirect(
            reverse('feature_settings_list', kwargs={'hotel_id': profile.hotel.id, 'profile_id': profile.id}))
    return HttpResponse("Method not supported")


def import_home_features_task(file_path, profile):
    json_data = open(file_path, 'r')
    data1 = json.load(json_data)  # deserialises it
    insert_list = []
    if len(data1) > 0:
        HomeFeatures.objects.filter(room_type=profile).delete()
        for obj_data in data1:
            print("Inner.. %s" % obj_data)
            m = HomeFeatures(**obj_data)
            m.room_type = profile
            insert_list.append(m)
        HomeFeatures.objects.bulk_create(insert_list)  # Success in performance


@permission_required("ipad_config.change_homefeatures")
def import_home_features(request):
    if request.method == 'POST' and request.FILES['home_features_json']:
        profile_type = request.POST['profile_type']
        profile = RoomType.objects.get(pk=profile_type)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["home_features_json"].chunks():
                f.write(chunk)

            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "HOME_FEATURE"
            queue.state = "PENDING"
            queue.room_type = profile
            queue.save()
            upload_task.delay()

        return redirect(
            reverse('home_feature_settings_list', kwargs={'hotel_id': profile.hotel.id, 'profile_id': profile.id}))
    return HttpResponse("Method not supported")


@permission_required("")
def import_seed_sql(request):
    if request.method == 'POST' and request.FILES['seed_file']:
        seed_file = request.FILES['seed_file']
        data = seed_file.read()
        seed_file.seek(0)
        from django.db import connections
        cursor = connections['default'].cursor()
        cursor.execute(data)
        return HttpResponse("Uploaded")
    return HttpResponse("Method not supported")


def import_theme_seed(file_path, theme):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()

    seed_tables = {
        "time_zone": "TimeZone",
        "color_style": "ColorStyle",
        "color_style_mapping": "ColorStyleMapping",
        "font_style": "FontStyle",
        "font_style_mapping": "FontStyleMapping"
    }

    for key, model_name in seed_tables.items():

        try:
            cursor.execute("SELECT * from %s" % key)

            r = [dict((cursor.description[i][0], value)
                      for i, value in enumerate(row)) for row in cursor.fetchall()]
            my_query = (r[0] if r else None) if False else r
            obj_data_array = json.dumps(my_query)
            model = apps.get_model('ipad_config', model_name)
            if model_name in ['ColorStyle', 'ColorStyleMapping', 'FontStyle', 'FontStyleMapping']:
                model.objects.filter(theme=theme).delete()
            else:
                model.objects.all().delete()
            with transaction.atomic():
                insert_list = []
                for obj_data in json.loads(obj_data_array):
                    print("Inner.. %s" % obj_data)
                    if model_name in ['ColorStyle', 'FontStyle']:
                        obj_data.pop('id')
                    m = model(**obj_data)
                    if model_name in ['ColorStyle', 'ColorStyleMapping', 'FontStyle', 'FontStyleMapping']:
                        m.theme = theme
                    insert_list.append(m)
                model.objects.bulk_create(insert_list)  # Success in performance
        except OperationalError as ex:
            print(ex)
            raise
    print("import success")


def import_airport_details_seed(file_path):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()

    seed_tables = {
        # "airlinedetails": "AirlineDetail",
        "airportDetails": "AirportDetail",
    }

    for key, model_name in seed_tables.items():

        try:
            cursor.execute("SELECT * from %s" % key)
            r = [dict((cursor.description[i][0], value)
                      for i, value in enumerate(row)) for row in cursor.fetchall()]
            my_query = (r[0] if r else None) if False else r
            obj_data_array = json.dumps(my_query)
            model = apps.get_model('ipad_config', model_name)
            # model.objects.all().delete()
            with transaction.atomic():
                insert_list = []
                for obj_data in json.loads(obj_data_array):
                    print("Inner.. %s" % obj_data)
                    try:
                        airport = model.objects.get(airport_code=obj_data['airport_code'],
                                                    city_code=obj_data['city_code'])
                        print("already exist")
                        airport.airport_name = obj_data['airport_name']
                        airport.country = obj_data['country']
                        airport.city = obj_data['city']
                        airport.location = obj_data['location']
                        airport.status = obj_data['status']
                        airport.position = obj_data['position']
                        airport.save()

                    except ObjectDoesNotExist:
                        print("New entry found")
                        m = model(**obj_data)
                        # m.save()
                        insert_list.append(m)
                model.objects.bulk_create(insert_list)  # Success in performance
        except OperationalError as ex:
            print(ex)
            raise
    print("import success")


def import_airline_details_seed(file_path):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()

    seed_tables = {
        "airlinedetails": "AirlineDetail",
    }

    for key, model_name in seed_tables.items():

        try:
            cursor.execute("SELECT * from %s" % key)
            r = [dict((cursor.description[i][0], value)
                      for i, value in enumerate(row)) for row in cursor.fetchall()]
            my_query = (r[0] if r else None) if False else r
            obj_data_array = json.dumps(my_query)
            model = apps.get_model('ipad_config', model_name)
            # model.objects.all().delete()
            with transaction.atomic():
                insert_list = []
                for obj_data in json.loads(obj_data_array):
                    print("Inner.. %s" % obj_data)
                    try:
                        airline = model.objects.get(airlineCode=obj_data['airlineCode'])
                        print("already exist")
                        airline.airlineName = obj_data['airlineName']
                        airline.imageName = obj_data['imageName']
                        airline.position = obj_data['position']
                        airline.save()
                    except ObjectDoesNotExist:
                        print("New entry found")
                        m = model(**obj_data)
                        # m.save()
                        insert_list.append(m)
                model.objects.bulk_create(insert_list)  # Success in performance
        except OperationalError as ex:
            print(ex)
            raise
    print("import success")


@app.task
def upload_task():
    if UploadQueue.objects.filter(state="RUNNING").exists():
        pass
    else:
        for queue in UploadQueue.objects.filter(state="PENDING")[:1]:
            queue.state = "RUNNING"
            queue.save()
            try:
                if queue.upload_type == "THEME":
                    theme = Theme.objects.get(id=queue.theme_id)
                    import_theme_seed(queue.file_path, theme)
                elif queue.upload_type == "MAIN_FEATURES":
                    import_main_feature_task(queue.file_path, queue.room_type)
                elif queue.upload_type == "LANGUAGE":
                    language_seed(queue.file_path)
                elif queue.upload_type == "COMMON_SETTINGS":
                    import_common_settings_task(queue.file_path, queue.room_type)
                elif queue.upload_type == "FEATURE_SETTINGS":
                    import_feature_settings_task(queue.file_path, queue.room_type)
                elif queue.upload_type == "HOME_FEATURE":
                    import_home_features_task(queue.file_path, queue.room_type)
                elif queue.upload_type == "ASSET_ZIP":
                    import_asset_zip_task(queue.file_path, queue.theme_id)
                elif queue.upload_type == "AIRPORT_DETAILS":
                    import_airport_details_seed(queue.file_path)
                elif queue.upload_type == "AIRLINE_DETAILS":
                    import_airline_details_seed(queue.file_path)

                queue.state = "SUCCESS"
                queue.save()
            except Exception as e:
                print(e)
                queue.state = "FAILED"
                queue.error = str(e)
                queue.save()


@permission_required("ipad_config.change_theme")
def import_seed(request):
    if request.method == 'POST' and request.FILES['theme_file']:

        theme_id = request.POST['theme']
        theme = Theme.objects.get(id=theme_id)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["theme_file"].chunks():
                f.write(chunk)
        queue = UploadQueue()
        queue.file_path = f.name
        queue.upload_type = "THEME"
        queue.theme_id = theme.id
        queue.state = "PENDING"
        queue.save()
        upload_task.delay()
        return redirect(reverse('theme_details', kwargs={'theme_id': theme.id}))
    themes = Theme.objects.all()
    return render(request, 'pages/hotels/upload_settings.html', {'themes': themes})


def save_fqdn(server_type, fqdn=None):
    if fqdn:
        try:
            fqdn_row = FQDN.objects.get(server=server_type)
            fqdn_row.fqdn = fqdn
            fqdn_row.save()
        except ObjectDoesNotExist:
            f = FQDN(server=server_type, fqdn=fqdn)
            f.save()


@permission_required("ipad_config.view_staticcontent")
def hotel_staticcontent_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    static_contents = hotel.static_content.all()
    form = HotelStaticContentForm(initial={'hotel': hotel})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            static_contents = static_contents.filter(
                Q(content__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass

    page = request.GET.get('page', 1)
    paginator = Paginator(static_contents.order_by('-added_on'), 10)
    try:
        static_contents = paginator.page(page)
    except PageNotAnInteger:
        static_contents = paginator.page(1)
    except EmptyPage:
        static_contents = paginator.page(paginator.num_pages)

    return render(request, 'pages/hotels/hotel_staticcontent_list.html', {
        'hotel': hotel,
        'static_contents': static_contents,
        'form': form
    })


@permission_required("ipad_config.change_staticcontent")
def hotel_staticcontent_edit(request, hotel_id, staticcontent_id=None):
    hotel = Hotel.objects.get(id=hotel_id)
    static_content = StaticContent.objects.none()
    form = HotelStaticContentForm()
    if staticcontent_id:
        static_content = StaticContent.objects.get(pk=staticcontent_id)
        form = HotelStaticContentForm(instance=static_content)
    is_add_action_failed = False
    if request.POST:
        print(request.POST)
        if staticcontent_id:
            if request.FILES:
                if os.path.exists(MEDIA_ROOT + "/" + static_content.content.name):
                    os.remove(MEDIA_ROOT + "/" + static_content.content.name)
            form = HotelStaticContentForm(request.POST, request.FILES, instance=static_content)
        else:
            is_add_action_failed = True
            form = HotelStaticContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('hotel_staticcontent_list', kwargs={'hotel_id': hotel_id}))
        else:
            static_contents = hotel.static_content.all()
            template = 'pages/hotels/hotel_staticcontent_list.html' if is_add_action_failed else \
                'pages/hotels/hotel_staticcontent_form.html'
            return render(request, template, {
                'hotel': hotel,
                'static_contents': static_contents,
                'form': form,
                'static_content': static_content,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/hotels/hotel_staticcontent_form.html',
                  {
                      'form': form,
                      'hotel': hotel,
                      'static_content': static_content
                  }
                  )


@permission_required("ipad_config.change_staticcontent")
def hotel_staticcontent_delete(request, hotel_id, staticcontent_id):
    obj = StaticContent.objects.filter(id=staticcontent_id)
    if obj.exists():
        if os.path.exists(MEDIA_ROOT + "/" + obj.first().content.name):
            os.remove(MEDIA_ROOT + "/" + obj.first().content.name)
        obj.delete()
    return redirect(reverse('hotel_staticcontent_list', kwargs={"hotel_id": hotel_id}))


@permission_required("ipad_config.view_hotelimages")
def hotel_image_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    hotel_images = hotel.hotel_images.all()
    form = HotelImageForm(initial={'hotel': hotel})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            hotel_images = hotel_images.filter(
                Q(assetName__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass

    page = request.GET.get('page', 1)
    paginator = Paginator(hotel_images, 10)
    try:
        hotel_images = paginator.page(page)
    except PageNotAnInteger:
        hotel_images = paginator.page(1)
    except EmptyPage:
        hotel_images = paginator.page(paginator.num_pages)

    return render(request, 'pages/hotels/hotel_image_list.html', {
        'hotel': hotel,
        'hotel_images': hotel_images,
        'form': form
    })


@permission_required("ipad_config.change_hotelimages")
def hotel_image_edit(request, hotel_id, image_id=None):
    hotel = Hotel.objects.get(id=hotel_id)

    form = HotelImageForm()
    hotel_image = None
    if image_id:
        hotel_image = HotelImages.objects.get(pk=image_id)
        form = HotelImageForm(instance=hotel_image)
    is_add_action_failed = False
    if request.POST:

        if image_id:
            if request.FILES:
                if os.path.exists(MEDIA_ROOT + "/" + hotel_image.assetName.name):
                    os.remove(MEDIA_ROOT + "/" + hotel_image.assetName.name)
            form = HotelImageForm(request.POST, request.FILES, instance=hotel_image)
        else:
            is_add_action_failed = True
            form = HotelImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('hotel_image_list', kwargs={'hotel_id': hotel_id}))
        else:
            hotel_images = hotel.hotel_images.all()
            template = 'pages/hotels/hotel_image_list.html' if is_add_action_failed else \
                'pages/hotels/hotel_image_form.html'
            return render(request, template, {
                'hotel': hotel,
                'hotel_images': hotel_images,
                'form': form,
                'hotel_image': hotel_image,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/hotels/hotel_image_form.html',
                  {
                      'form': form,
                      'hotel': hotel,
                      'hotel_image': hotel_image
                  }
                  )


@permission_required("ipad_config.view_hotelairportdetail")
def hotel_airportdetail_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    airportdetails = hotel.hotel_airport_details.all()
    form = HotelAirportDetailForm(initial={'hotel': hotel})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            airportdetails = airportdetails.filter(
                Q(airport__airport_name__icontains=search_text) |
                Q(airport__country__icontains=search_text) |
                Q(airport__airport_code__icontains=search_text)
            )
        except Exception as e:
            print(str(e))

    page = request.GET.get('page', 1)
    paginator = Paginator(airportdetails, 10)
    try:
        airportdetails = paginator.page(page)
    except PageNotAnInteger:
        airportdetails = paginator.page(1)
    except EmptyPage:
        airportdetails = paginator.page(paginator.num_pages)

    return render(request, 'pages/hotels/hotel_airportdetails_list.html', {
        'hotel': hotel,
        'airportdetails': airportdetails,
        'form': form
    })


@permission_required("ipad_config.change_hotelairportdetail")
def hotel_airportdetail_edit(request, hotel_id, airport_id=None):
    hotel = Hotel.objects.get(id=hotel_id)

    form = HotelAirportDetailForm()
    airport = None
    if airport_id:
        airport = HotelAirportDetail.objects.get(pk=airport_id)
        form = HotelAirportDetailForm(instance=airport)
    is_add_action_failed = False
    if request.POST:
        if airport_id:
            form = HotelAirportDetailForm(request.POST, instance=airport)
        else:
            is_add_action_failed = True
            form = HotelAirportDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('hotel_airportdetail_list', kwargs={'hotel_id': hotel_id}))
        else:
            airportdetails = hotel.hotel_airport_details.all()
            template = 'pages/hotels/hotel_airportdetails_list.html' if is_add_action_failed else \
                'pages/hotels/hotel_airportdetails_form.html'
            return render(request, template, {
                'hotel': hotel,
                'airportdetails': airportdetails,
                'form': form,
                'airport': airport,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/hotels/hotel_airportdetails_form.html',
                  {
                      'form': form,
                      'hotel': hotel,
                      'airport': airport
                  }
                  )


@permission_required("ipad_config.delete_hotelairportdetail")
def hotel_airportdetail_delete(request, hotel_id, airport_id):
    airport = HotelAirportDetail.objects.get(pk=airport_id)
    airport.delete()

    return redirect(reverse('hotel_airportdetail_list', kwargs={'hotel_id': hotel_id}))


@permission_required("ipad_config.view_dvhotellanguage")
def hotel_language_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    languages = hotel.languages.all().order_by('tag')
    form = HotelLanguageForm(initial={'hotel': hotel})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            languages = languages.filter(
                Q(tag__icontains=search_text) |
                Q(field__icontains=search_text)
            )
        except Exception as e:
            print(str(e))

    page = request.GET.get('page', 1)
    paginator = Paginator(languages, 10)
    try:
        languages = paginator.page(page)
    except PageNotAnInteger:
        languages = paginator.page(1)
    except EmptyPage:
        languages = paginator.page(paginator.num_pages)

    return render(request, 'pages/hotels/hotel_language_list.html', {
        'hotel': hotel,
        'languages': languages,
        'form': form
    })


@permission_required("ipad_config.change_dvhotellanguage")
def hotel_language_edit(request, hotel_id, language_id=None):
    hotel = Hotel.objects.get(id=hotel_id)

    form = HotelLanguageForm()
    language = None
    if language_id:
        language = DVHotelLanguage.objects.get(pk=language_id)
        form = HotelLanguageForm(instance=language)
    is_add_action_failed = False
    if request.POST:
        if language_id:
            form = HotelLanguageForm(request.POST, instance=language)
        else:
            is_add_action_failed = True
            form = HotelLanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('hotel_language_list', kwargs={'hotel_id': hotel_id}))
        else:
            languages = hotel.languages.all()
            template = 'pages/hotels/hotel_language_list.html' if is_add_action_failed else \
                'pages/hotels/hotel_language_form.html'
            return render(request, template, {
                'hotel': hotel,
                'languages': languages,
                'form': form,
                'language': language,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/hotels/hotel_language_form.html',
                  {
                      'form': form,
                      'hotel': hotel,
                      'language': language
                  }
                  )


@permission_required("ipad_config.delete_dvhotellanguage")
def hotel_language_delete(request, hotel_id, language_id):
    language = DVHotelLanguage.objects.get(pk=language_id)
    language.delete()

    return redirect(reverse('hotel_language_list', kwargs={'hotel_id': hotel_id}))


@permission_required("ipad_config.view_dvhotellanguagecode")
def hotel_language_code_list(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    language_codes = hotel.hotel_langauge_codes.all().extra(\
        select={'position_int': "CAST(substring(position FROM '^[0-9]+') AS INTEGER)"}).\
        order_by('position_int')
    form = HotelLanguageCodeForm(initial={'hotel': hotel})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            language_codes = language_codes.filter(
                Q(language_code__lang_code__icontains=search_text) |
                Q(language_code__display_name__icontains=search_text)
            )
        except Exception as e:
            print(str(e))

    page = request.GET.get('page', 1)
    paginator = Paginator(language_codes, 10)
    try:
        language_codes = paginator.page(page)
    except PageNotAnInteger:
        language_codes = paginator.page(1)
    except EmptyPage:
        language_codes = paginator.page(paginator.num_pages)

    return render(request, 'pages/hotels/hotel_language_code_list.html', {
        'hotel': hotel,
        'language_codes': language_codes,
        'form': form
    })


@permission_required("ipad_config.change_dvhotellanguagecode")
def hotel_language_code_edit(request, hotel_id, language_code_id=None):
    hotel = Hotel.objects.get(id=hotel_id)

    form = HotelLanguageCodeForm()
    language_code = None
    if language_code_id:
        language_code = DVHotelLanguageCode.objects.get(pk=language_code_id)
        form = HotelLanguageCodeForm(instance=language_code)
    is_add_action_failed = False
    if request.POST:
        if language_code_id:
            form = HotelLanguageCodeForm(request.POST, instance=language_code)
        else:
            is_add_action_failed = True
            form = HotelLanguageCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('hotel_language_code_list', kwargs={'hotel_id': hotel_id}))
        else:
            language_codes = hotel.languages.all()
            template = 'pages/hotels/hotel_language_code_list.html' if is_add_action_failed else \
                'pages/hotels/hotel_language_code_form.html'
            return render(request, template, {
                'hotel': hotel,
                'language_codes': language_codes,
                'form': form,
                'language_code': language_code,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/hotels/hotel_language_code_form.html',
                  {
                      'form': form,
                      'hotel': hotel,
                      'language_code': language_code
                  }
                  )


@permission_required("ipad_config.delete_dvhotellanguagecode")
def hotel_language_code_delete(request, hotel_id, language_code_id):
    language_code = DVHotelLanguageCode.objects.get(pk=language_code_id)
    language_code.delete()

    return redirect(reverse('hotel_language_code_list', kwargs={'hotel_id': hotel_id}))


@permission_required("ipad_config.add_hotel")
def sync_fqdn(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    change_messages = []
    try:
        hotel_dict, fqdn, theme_name = get_hotel_synced(hotel.hotel_key)
        for key, value in fqdn.items():
            try:
                obj = FQDN.objects.get(hotel=hotel, server=key)
                obj.fqdn = value
                obj.save()
            except ObjectDoesNotExist:

                FQDN(hotel=hotel, server=key, fqdn=value).save()
        change_messages.append({'tags': "debug", 'message': "FQDNs successfully synced!"})
    except Exception as e:
        change_messages.append({'tags': "error", 'message': "Could not sync fqdn, " + str(e)})

    fqdns_data = FQDN.objects.filter(hotel=hotel)
    fqdn_dict = {}
    for fqdn in fqdns_data:
        fqdn_dict[fqdn.server] = fqdn.fqdn
    return render(request, 'pages/hotels/fqdns.html', {
        'fqdns': fqdn_dict,
        'hotel': hotel,
        'messages': change_messages
    })


@permission_required("ipad_config.change_fqdn")
def fqdns(request, hotel_id):
    if request.method == 'POST':
        if request.POST['dvs_fqdn']:
            save_fqdn('DVS', request.POST['dvs_fqdn'])

        if request.POST['das_fqdn']:
            save_fqdn('DAS', request.POST['das_fqdn'])

        if request.POST['his_fqdn']:
            save_fqdn('HIS', request.POST['his_fqdn'])

        if request.POST['mds_fqdn']:
            save_fqdn('MDS', request.POST['mds_fqdn'])

        if request.POST['vod_fqdn']:
            save_fqdn('VOD', request.POST['vod_fqdn'])

        if request.POST['butler_fqdn']:
            save_fqdn('BUTLER', request.POST['butler_fqdn'])

        if request.POST['analytics_fqdn']:
            save_fqdn('ANALYTICS', request.POST['analytics_fqdn'])

        messages.add_message(request, messages.SUCCESS, 'FQDNs saved successfully!')

    hotel = Hotel.objects.get(pk=hotel_id)
    fqdns_data = FQDN.objects.filter(hotel=hotel)
    fqdn_dict = {}
    for fqdn in fqdns_data:
        fqdn_dict[fqdn.server] = fqdn.fqdn

    return render(request, 'pages/hotels/fqdns.html', {
        'fqdns': fqdn_dict,
        'hotel': hotel
    })


def get_java_variables():
    tag_list = []
    fqdn_obj = {}
    for f in FQDN.objects.all():
        fqdn_obj[f.server] = f.fqdn
    for obj in JavaEnvironmentVariable.objects.all():
        data = {"id": obj.id, "key": obj.key, "value": obj.value.format(**fqdn_obj)}
        tag_list.append(data)

    return tag_list


@permission_required("")
def dgjava(request):
    var = get_java_variables()
    return render(request, 'pages/hotels/dgjava.html', {"variables": var})


@permission_required("")
def generate_dgjava(request):
    var = get_java_variables()
    return render(request, 'pages/hotels/dgjava.txt', {"variables": var})


@permission_required("ipad_config.change_javaconfig")
def edit_java_env_variable(request, id):
    if request.method == 'POST':
        key = request.POST['key']
        val = request.POST['value']
        env_var = JavaEnvironmentVariable.objects.get(key=key)
        env_var.value = val
        env_var.save()
        return HttpResponseRedirect(reverse('dgjava'))

    else:
        env_var = JavaEnvironmentVariable.objects.get(id=id)
        return render(request, 'pages/hotels/dgjava_edit.html', {"obj": env_var})


def get_nodes(values, parant):
    if type(values) == dict:
        for key, value in values.items():
            a = AppConfigTag(key=key)
            if type(value) == dict:
                a.tag_type = "dict"
                if parant is not None:
                    a.parent = parant
                a.save()
                get_nodes(value, a)
            elif type(value) == list:
                a.tag_type = "list"
                if parant is not None:
                    a.parent = parant
                a.save()
                get_nodes(value, a)
            else:
                a.value = value
                if type(value) == int:
                    a.tag_type = "int"
                if type(value) == bool:
                    a.tag_type = "bool"
                if parant is not None:
                    a.parent = parant
                a.save()

    elif type(values) == list:
        for obj in values:
            get_nodes(obj, parant)

    else:
        a = AppConfigTag()
        a.value = values
        if type(values) == int:
            a.tag_type = "int"
        if type(values) == bool:
            a.tag_type = "bool"
        if parant is not None and type(parant) == AppConfigTag:
            a.parent = parant
        a.save()


def get_data(obj):
    if obj.tag_type == "list":
        d = {}
        value = []
        for child in obj.child_tags.all():
            if len(child.key) > 0:
                d[child.key] = get_data(child)
            else:
                value.append(get_data(child))
        if bool(d):
            value.append(d)
    elif obj.tag_type == "dict":
        value = {}
        for child in obj.child_tags.all():
            value[child.key] = get_data(child)
    elif obj.tag_type == "int":
        value = int(obj.value)
    elif obj.tag_type == "bool":
        if obj.value == "False":
            value = False
        else:
            value = True
    else:
        value = obj.value
    return value


@permission_required("")
def appconfig(request):
    url = "http://192.168.0.66:7990/projects/PP/repos/php-common-files/raw/digivalet-cms-dashboard-configuration/app-config.json?at=refs%2Fheads%2Fmaster"
    AppConfigTag.objects.all().delete()
    print(AppConfigTag.objects.count())
    r = requests.get(url, auth=('release_manager', 'dvserv3r@lucy'))
    if r.status_code == 200:
        response = r.json()
        get_nodes(response, None)
        # print(response)

    else:
        print(r)
        pass
    data = AppConfigTag.objects.filter(parent=None)
    obj = {}
    for tag in data:
        obj[tag.key] = get_data(tag)
    return render(request, 'pages/hotels/appconfig.html', {'response': json.dumps(obj)})


def language_seed(file_path):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()

    seed_tables = {
        "dv_language_code": "DVLanguageCode",
        "dv_language": "DVLanguage"
    }

    for key, model_name in seed_tables.items():

        try:
            cursor.execute("SELECT * from %s" % key)

            model = apps.get_model('ipad_config', model_name)
            if not model_name == 'DVLanguageCode':
                model.objects.all().delete()
            while True:
                two_rows = cursor.fetchmany(1000)
                if not two_rows:
                    break

                insert_list = []

                for row in two_rows:
                    row_dict = {}
                    for i, value in enumerate(row):
                        row_dict[cursor.description[i][0]] = value

                    if model_name == 'DVLanguageCode':
                        row_dict.pop('lang_id')

                    obj_data = {}
                    try:
                        obj_data = json.dumps(row_dict, ensure_ascii=False).encode('utf8')
                    except Exception as ex:
                        if model_name == 'DVLanguage':
                            row_dict['field'] = row_dict['field'].decode('utf-8')
                            obj_data = json.dumps(row_dict, ensure_ascii=False).encode('utf8')
                        print(ex)

                    with transaction.atomic():
                        obj_data = json.loads(obj_data)
                        print("Inner.. %s" % obj_data)
                        if model_name == 'DVLanguageCode' and DVLanguageCode.objects.filter(lang_code=obj_data["lang_code"]).exists():
                            continue
                        m = model(**obj_data)
                        insert_list.append(m)
                model.objects.bulk_create(insert_list)  # Success in performance

        except OperationalError as ex:
            print(ex)


@permission_required("ipad_config.change_dvlanguage")
def import_language_seed(request):
    items = DVLanguage.objects.all()
    language_form = DVLanguageForm()
    language_code_form = DVLanguageCodeForm()

    if request.method == "GET":

        try:
            lang_code = request.GET['lang_code']
            if lang_code:
                items = items.filter(lang_code=lang_code)
        except:
            pass

        try:
            search_text = request.GET['search_text']
            if search_text:
                items = items.filter(
                    Q(tag__icontains=search_text) |
                    Q(field__icontains=search_text) |
                    Q(lang_code__icontains=search_text)
                )
        except Exception as e:
            pass

    code_items = DVLanguageCode.objects.all().extra(
        select={'position_int': "CAST(substring(position FROM '^[0-9]+') AS INTEGER)"}).\
        order_by('position_int')

    items = paginate(request, items, 20)

    if request.method == 'POST' and request.FILES['seed_file']:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["seed_file"].chunks():
                f.write(chunk)
        queue = UploadQueue()
        queue.file_path = f.name
        queue.upload_type = "LANGUAGE"
        queue.state = "PENDING"
        queue.save()
        upload_task.delay()

    return render(request, 'pages/upload_language.html', {
        'items': items,
        'code_items': code_items,
        'language_form': language_form,
        'language_code_form': language_code_form
    })


@permission_required("ipad_config.change_hotelLanguageCode")
def import_hotel_language_code(request, hotel_id):
    if request.method == 'POST' and request.FILES['hotel_language_code']:
        file = request.FILES['hotel_language_code']
        hotel = Hotel.objects.get(pk=hotel_id)
        data = json.loads(file.read().decode('utf8'))
        with transaction.atomic():
            DVHotelLanguageCode.objects.filter(hotel=hotel).delete()
            for d in data:
                try:
                    language_code_obj = DVLanguageCode.objects.get(lang_code=d['lang_code'])
                    DVHotelLanguageCode.objects.create(hotel=hotel, language_code=language_code_obj,
                                                       position=d['position'], is_active=d['is_active'])

                except ObjectDoesNotExist:
                    pass

    return redirect(reverse('hotel_language_code_list', kwargs={'hotel_id': hotel_id}))


@permission_required("ipad_config.change_hotelLanguageCode")
def import_hotel_language(request, hotel_id):
    if request.method == 'POST' and request.FILES['hotel_language']:
        file = request.FILES['hotel_language']

        hotel = Hotel.objects.get(pk=hotel_id)
        data = json.loads(file.read().decode('utf8'))
        with transaction.atomic():
            DVHotelLanguage.objects.filter(hotel=hotel).delete()
            for d in data:
                DVHotelLanguage.objects.create(hotel=hotel, tag=d['tag'], module_name=d['module_name'],
                                               field=d['field'], lang_code=d['lang_code'])

    return redirect(reverse('hotel_language_list', kwargs={'hotel_id': hotel_id}))


def import_asset_zip_task(file_path, theme_id):
    z = zipfile.ZipFile(file_path)
    print(file_path)
    theme = Theme.objects.get(id=theme_id)
    insert_list = []
    path = MEDIA_ROOT + "/" + theme.path() + "/"
    for file in z.namelist():
        print(type(file))
        print(path + file)
        z.extract(file, path)
        if not file.endswith('/'):
            asset_image_name = file.split('/')
            asset_image_name = asset_image_name[len(asset_image_name) - 1]
            prefix = theme.path() + "/" + ASSET_LOCATION
            images = SettingsImages.objects.filter(assetName=prefix + asset_image_name, theme=theme)
            if len(images) <= 0:
                image = SettingsImages(assetName=prefix + asset_image_name, assetType="image")
                image.theme = theme
                # image.save()
                insert_list.append(image)
    SettingsImages.objects.bulk_create(insert_list)


@permission_required("ipad_config.change_theme")
def import_asset_zip(request):
    if request.method == 'POST' and request.FILES['setting_asset_zip']:
        theme_id = request.POST['theme_id']

        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["setting_asset_zip"].chunks():
                f.write(chunk)
            # import_asset_zip_task(f.name,theme_id)
            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "ASSET_ZIP"
            queue.state = "PENDING"
            queue.theme_id = theme_id
            queue.save()
            upload_task.delay()
        return redirect(reverse('setting_assets_list', kwargs={'theme_id': theme_id}))


# @permission_required("ipad_config.change_mainfeatures")


@permission_required("")
def index(request):
    hotels = Hotel.objects.all()
    upload_queues = UploadQueue.objects.all().order_by('-created_on')[:20]
    return render(request, 'pages/hotels/list.html',
                  {'hotels': hotels, 'upload_queues': upload_queues}
                  )


@permission_required("")
def hotel_details(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    # user = User.objects.get(pk=request.user.id)
    # b = HotelBookmark(user=user, hotel=hotel)
    # b.save()
    return redirect(reverse('ipad_profiles_list', kwargs={'hotel_id': hotel.id}))
    # return render(request, 'pages/hotels/details.html', { 'hotel': hotel })


def get_response_value(json_obj, key):
    try:
        value = json_obj[key]
        if value is not None:
            return value
        else:
            value = "Not Provided"
            return value
    except KeyError:
        raise


def get_hotel_synced(key):
    client = CloudClient()
    params = {'fields': "theme.name,*", 'status': "published", 'filter[hotel_key]': key, 'single': 1}
    response = client.make_get_request("/dvp/items/hotel_info", params)
    json_data = response.json()['data']

    hotel = {"hotel_name": get_response_value(json_data, "hotel_name"),
             "hotel_code": get_response_value(json_data, "hotel_code"),
             "hotel_id": get_response_value(json_data, "hotel_id")}

    # fqdn
    fqdn = {'DAS': get_response_value(json_data, "das_fqdn"), 'DVS': get_response_value(json_data, "dvs_fqdn"),
            'HIS': get_response_value(json_data, "his_fqdn"), 'MDS': get_response_value(json_data, "mds_fqdn"),
            'VOD': get_response_value(json_data, "vod_fqdn"),
            'ANALYTICS': get_response_value(json_data, "analytics_fqdn"),
            'BUTLER': get_response_value(json_data, "butler_fqdn")}

    # theme
    theme_name = get_response_value(json_data, "theme")
    theme_name = theme_name.get("name") if type(theme_name) == dict else theme_name

    return hotel, fqdn, theme_name


# /dvp/items/hotel_info?fields=*,theme.name,&
# status=published&
# filter[hotel_key]=$2y$10$Dbk/niZQD7XgFUTGNm7Ca.dJf8DBk7kCaaxpFrMtMlU12LRt1znPi
# &single=1

def upload_profile_defaults(profile):
    default_obj = DefaultImportSetting.load()
    queue = UploadQueue()
    queue.file_path = default_obj.main_features.path
    queue.upload_type = "MAIN_FEATURES"
    queue.state = "PENDING"
    queue.room_type = profile
    queue.save()

    queue2 = UploadQueue()
    queue2.file_path = default_obj.common_settings.path
    queue2.upload_type = "COMMON_SETTINGS"
    queue2.state = "PENDING"
    queue2.room_type = profile
    queue2.save()

    queue3 = UploadQueue()
    queue3.file_path = default_obj.feature_settings.path
    queue3.upload_type = "FEATURE_SETTINGS"
    queue3.state = "PENDING"
    queue3.room_type = profile
    queue3.save()

    queue4 = UploadQueue()
    queue4.file_path = default_obj.home_feature_settings.path
    queue4.upload_type = "HOME_FEATURE"
    queue4.state = "PENDING"
    queue4.room_type = profile
    queue4.save()

    # queue4 = UploadQueue()
    # queue4.file_path = default_obj.language_sqlite.path
    # queue4.upload_type = "LANGUAGE"
    # queue4.state = "PENDING"
    # queue4.room_type = profile
    # queue4.save()


def upload_theme_defaults(theme_id):
    default_obj = DefaultImportSetting.load()
    queue = UploadQueue()
    queue.file_path = default_obj.theme_sqlite.path
    queue.upload_type = "THEME"
    queue.theme_id = theme_id
    queue.state = "PENDING"
    queue.save()

    queue2 = UploadQueue()
    queue2.file_path = default_obj.setting_assets.path
    queue2.upload_type = "ASSET_ZIP"
    queue2.state = "PENDING"
    queue2.theme_id = theme_id
    queue2.save()


@permission_required("ipad_config.add_hotel")
def add_hotel(request):
    # Sync hotel information from outside.
    # Import default main features, feature settings, home features and common settings.
    alert = []
    if request.method == 'POST':
        key = request.POST['key']

        try:

            hotel_dict, fqdn, theme_name = get_hotel_synced(key)
            try:
                hotel = Hotel.objects.get(hotel_key=key)
                hotel.name = hotel_dict['hotel_name']
                hotel.hotel_code = hotel_dict['hotel_code']
                hotel.hotel_id = hotel_dict['hotel_id']
                hotel.save()
            except ObjectDoesNotExist:
                hotel = Hotel(name=hotel_dict['hotel_name'], hotel_code=hotel_dict['hotel_code'],
                              hotel_id=hotel_dict['hotel_id'], hotel_key=key)
                hotel.save()

                for key, value in fqdn.items():
                    try:
                        obj = FQDN.objects.get(hotel=hotel, server=key)
                        obj.fqdn = value
                        obj.save()
                    except ObjectDoesNotExist:
                        FQDN(hotel=hotel, server=key, fqdn=value).save()

                try:
                    theme = Theme.objects.get(name=theme_name)
                except ObjectDoesNotExist:
                    theme = Theme(name=theme_name)
                    theme.save()
                    upload_theme_defaults(theme.id)
                    upload_task.delay()
                # Create default profile.
                rt = RoomType(hotel=hotel, name='default', theme=theme)
                rt.save()
                upload_profile_defaults(rt)
                upload_task.delay()
                upload_java_configs(hotel, DefaultImportSetting.load().java_config_json.path, request)
                return redirect('index')

        except Exception as e:
            alert.append({'tags': "error", 'message': "Could not sync hotel details , " + str(e)})
            print(e)
    return render(request, 'pages/hotels/add.html', {'messages': alert})


@api_view(['GET', ])
def get_content(request, hotel_code):
    user = request.user
    hotel = Hotel.objects.get(hotel_code=hotel_code)

    if not hotel.is_last_publish_success():
        return Response(data={"message": "Profile publish was not successfull."}, status=status.HTTP_204_NO_CONTENT)
    if 'update_type' not in request.GET:
        return Response(data={"message": "Update type not provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if not user.is_superuser:
            user_hotel = user.user_hotels.all().get(hotel=hotel)
    except ObjectDoesNotExist as e:
        print(e)
        return HttpResponseForbidden()

    res = {}
    profile_types = []
    update_type = request.GET['update_type']
    # settings sqlite
    for room_type in hotel.room_types.all():
        obj = {}
        type_name = '' if room_type.name == "default" else room_type.name + "/"
        obj['type'] = room_type.name
        content = []
        location = MEDIA_URL + str(hotel.id) + "/" + type_name
        if update_type in ["ALL", "SQLITES", "SQLITE_WITH_ASSETS"]:
            content.append({
                "name": "settings.sqlite",
                "dir": type_name,
                "url": request.scheme + "://" + request.get_host() + location + "settings.sqlite"
            })
        if update_type in ["ALL", "LANGAUGE"]:
            content.append({
                "name": "language.sqlite",
                "dir": type_name,
                "url": request.scheme + "://" + request.get_host() + location + "language.sqlite"
            })
        if update_type in ["ALL", "SQLITE_WITH_ASSETS"]:
            content.append({
                "name": "assets.json",
                "dir": type_name + "setting_images/",
                "url": request.scheme + "://" + request.get_host() + location + "setting_images/assets.json"
            })
        obj['content'] = content
        profile_types.append(obj)
    res['profiles'] = profile_types
    static_contents = []
    if update_type in ["ALL", "STATIC_CONTENT"]:
        for static_content in hotel.static_content.all():
            obj = {'file_type': static_content.file_type,
                   'url': request.scheme + "://" + request.get_host() + static_content.content.url}
            if static_content.room_type:
                obj['dir'] = '' if static_content.room_type.name == 'default' else static_content.room_type.name
            else:
                obj['dir'] = ""
            name = static_content.content.name.split("/")
            obj['name'] = name[len(name) - 1]
            static_contents.append(obj)
    res["static_content"] = static_contents
    return Response(res)


@permission_required("")
def shortcuts(request):
    return render(request, 'pages/shortcuts.html', {})


class CreateActiveUser(APIView):
    """
        API to create active user through API used during
        installation of mars client on site.
        """

    permission_classes = []

    def post(self, request):

        if not request.user.is_superuser:
            return Response({"status": False, "message": "You are not authorized to create user"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data.get("username", "password"):
            return Response({"status": False, "message": "Please Provide username and Password"},
                            status=status.HTTP_204_NO_CONTENT)

        try:
            User.objects.create_user(username=request.data["username"],
                                     password=request.data["password"])
            return Response({"status": True, "message": "User Created"},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print(str(e))
            return Response({"status": False, "message": "User Already Present"},
                            status=status.HTTP_409_CONFLICT)
