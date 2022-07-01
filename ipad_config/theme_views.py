"""
Created on 28-Dec-2019

@author: Vaibhav-Mahajan
"""

# Python Imports
import tempfile
import os
import shutil

# Django Imports
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, reverse
from django.db.models import Q

# Project Imports
from .models import Theme, FontStyle, FontStyleMapping, ColorStyle, ColorStyleMapping, AirlineDetail, SettingsImages, \
    AirportDetail, UploadQueue
from .forms import ThemeForm, FormStyleForm, FontStyleMappingForm, ColorStyleForm, ColorStyleMappingForm, \
    AirlineDetailForm, AirportDetailForm, SettingsImagesForm
from .views import upload_theme_defaults, upload_task
from .middlewares import permission_required
from config.settings.base import MEDIA_ROOT
from .utils import paginate


@permission_required("")
def theme_home(request):
    themes = Theme.objects.all()
    return render(request, 'pages/theme/list.html', {'themes': themes})


@permission_required({"ipad_config.add_theme", "ipad_config.change_theme"})
def add_theme(request, theme_id=None):
    title = "Add Theme"
    theme = None
    if theme_id:
        title = "Edit Theme"
        theme = Theme.objects.get(pk=theme_id)

    if request.POST:

        if theme:
            form = ThemeForm(request.POST, instance=theme)
        else:
            form = ThemeForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if not theme:
                print(obj.id)
                upload_theme_defaults(obj.id)

            return redirect(reverse('theme_home'))

        else:
            return render(request, 'pages/theme/theme_form.html', {'form': form, 'title': title})
    else:
        form = ThemeForm()
        if theme:
            title = "Edit Theme"
            form = ThemeForm(instance=theme)
        return render(request, 'pages/theme/theme_form.html', {'form': form, 'title': title})


@permission_required("")
def theme_details(request, theme_id):
    theme = Theme.objects.get(pk=theme_id)
    return render(request, 'pages/theme/details.html', {'theme': theme})


@permission_required("")
def color_style_list(request, theme_id):
    theme = Theme.objects.get(pk=theme_id)
    color_styles = theme.color_styles.all().order_by("color_style_name", "lang_code")
    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            color_styles = color_styles.filter(
                Q(color_style_name__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass

    color_styles = paginate(request, color_styles, 30)

    return render(request, 'pages/theme/color_style_list.html', {'theme': theme, 'color_styles': color_styles})


@permission_required("")
def color_style_mapping_list(request, theme_id):
    theme = Theme.objects.get(pk=theme_id)
    color_style_mappings = theme.color_style_mappings.all()
    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            color_style_mappings = color_style_mappings.filter(
                Q(color_style_name__icontains=search_text) |
                Q(module_name__icontains=search_text) |
                Q(apply_on__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass
    color_style_mappings = paginate(request, color_style_mappings, 30)

    return render(request, 'pages/theme/color_style_mapping_list.html',
                  {'theme': theme, 'color_style_mappings': color_style_mappings})


@permission_required("")
def font_style_list(request, theme_id):
    theme = Theme.objects.get(pk=theme_id)
    font_styles = theme.font_styles.all().order_by("font_style_name", "lang_code")
    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            font_styles = font_styles.filter(
                Q(font_style_name__icontains=search_text) |
                Q(lang_code__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass
    font_styles = paginate(request, font_styles, 30)

    return render(request, 'pages/theme/font_style_list.html', {'theme': theme, 'font_styles': font_styles})


@permission_required("")
def add_font_style(request, theme_id, font_style_id=None):
    title = "Add Font Style"
    theme = Theme.objects.get(pk=theme_id)
    font_style = None
    if font_style_id:
        title = "Edit Font Style"
        font_style = FontStyle.objects.get(pk=font_style_id)

    if request.POST:
        if font_style:
            form = FormStyleForm(request.POST, instance=font_style)
        else:
            form = FormStyleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('font_styles', kwargs={'theme_id': theme.id}))
        else:
            if font_style:
                return render(request, 'pages/theme/font_style_form.html',
                              {'form': form, 'title': title, 'theme': theme, 'font_style': font_style})
            return render(request, 'pages/theme/font_style_form.html', {'form': form, 'title': title, 'theme': theme})
    else:
        form = FormStyleForm()
        if font_style:
            title = "Edit Font Style"
            form = FormStyleForm(instance=font_style)
            return render(request, 'pages/theme/font_style_form.html',
                          {'form': form, 'title': title, 'theme': theme, 'font_style': font_style})
        return render(request, 'pages/theme/font_style_form.html', {'form': form, 'title': title, 'theme': theme})


@permission_required("")
def font_style_mapping_list(request, theme_id):
    theme = Theme.objects.get(pk=theme_id)
    font_style_mappings = theme.font_style_mappings.all()
    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            font_style_mappings = font_style_mappings.filter(
                Q(font_style_name__icontains=search_text) |
                Q(module_name__icontains=search_text) |
                Q(apply_on__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass
    font_style_mappings = paginate(request, font_style_mappings, 30)

    return render(request, 'pages/theme/font_style_mapping_list.html',
                  {'theme': theme, 'font_style_mappings': font_style_mappings})


@permission_required("ipad_config.change_theme")
def add_font_style_mapping(request, theme_id, font_style_mapping_id=None):
    title = "Add Font Style Mapping"
    theme = Theme.objects.get(pk=theme_id)
    font_style_mapping = None
    if font_style_mapping_id:
        title = "Edit Font Style Mapping"
        font_style_mapping = FontStyleMapping.objects.get(pk=font_style_mapping_id)

    if request.POST:
        if font_style_mapping:
            form = FontStyleMappingForm(request.POST, instance=font_style_mapping)
        else:
            form = FontStyleMappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('font_style_mappings', kwargs={'theme_id': theme.id}))
        else:
            if font_style_mapping:
                return render(request, 'pages/theme/font_style_mapping_form.html',
                              {'form': form, 'title': title, 'theme': theme})
            return render(request, 'pages/theme/font_style_mapping_form.html',
                          {'form': form, 'title': title, 'theme': theme})
    else:
        form = FontStyleMappingForm()
        if font_style_mapping:
            title = "Edit Font Style Mapping"
            form = FontStyleMappingForm(instance=font_style_mapping)
            return render(request, 'pages/theme/font_style_mapping_form.html',
                          {'form': form, 'title': title, 'theme': theme})
        return render(request, 'pages/theme/font_style_mapping_form.html',
                      {'form': form, 'title': title, 'theme': theme})


@permission_required("ipad_config.change_theme")
def add_color_style(request, theme_id, color_style_id=None):
    title = "Add Color Style"
    theme = Theme.objects.get(pk=theme_id)
    color_style = None
    if color_style_id:
        title = "Edit Color Style"
        color_style = ColorStyle.objects.get(pk=color_style_id)

    if request.POST:
        if color_style:
            form = ColorStyleForm(request.POST, instance=color_style)
        else:
            form = ColorStyleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('color_styles', kwargs={'theme_id': theme.id}))
        else:
            return render(request, 'pages/theme/color_style_form.html', {'form': form, 'title': title, 'theme': theme})
    else:
        form = ColorStyleForm()
        if color_style:
            title = "Edit Color Style"
            form = ColorStyleForm(instance=color_style)
        return render(request, 'pages/theme/color_style_form.html', {'form': form, 'title': title, 'theme': theme})


@permission_required("ipad_config.change_theme")
def add_color_style_mapping(request, theme_id, color_style_mapping_id=None):
    title = "Add Color Style Mapping"
    theme = Theme.objects.get(pk=theme_id)
    color_style_mapping = None
    if color_style_mapping_id:
        title = "Edit Color Style Mapping"
        color_style_mapping = ColorStyleMapping.objects.get(pk=color_style_mapping_id)

    if request.POST:
        if color_style_mapping:
            form = ColorStyleMappingForm(request.POST, instance=color_style_mapping)
        else:
            form = ColorStyleMappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('color_style_mappings', kwargs={'theme_id': theme.id}))
        else:
            return render(request, 'pages/theme/color_style_mapping_form.html',
                          {'form': form, 'title': title, 'theme': theme})
    else:
        form = ColorStyleMappingForm()
        if color_style_mapping:
            title = "Edit Color Style Mapping"
            form = ColorStyleMappingForm(instance=color_style_mapping)
        return render(request, 'pages/theme/color_style_mapping_form.html',
                      {'form': form, 'title': title, 'theme': theme})


@permission_required("ipad_config.bulk_delete_settingassets")
def setting_asset_bulkdelete(request, theme_id):
    if 'asset_id' in request.POST:
        data = dict(request.POST)
        for asset_id in data["asset_id"]:
            try:
                image = SettingsImages.objects.get(pk=asset_id)
                image.assetName.delete()
                image.delete()
            except Exception as e:
                print(e)

    return redirect(reverse('setting_assets_list', kwargs={'theme_id': theme_id}))


@permission_required("ipad_config.delete_settingsimages")
def setting_asset_delete(request, theme_id, asset_id):
    try:
        image = SettingsImages.objects.get(pk=asset_id)
        image.assetName.delete()
        image.delete()
    except Exception as e:
        print(str(e))
        pass
    return redirect(reverse('setting_assets_list', kwargs={'theme_id': theme_id}))


@permission_required("")
def setting_assets_list(request, theme_id):
    theme = Theme.objects.get(pk=theme_id)
    setting_assets = theme.settings_images.all().distinct('assetName')

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            setting_assets = setting_assets.filter(
                Q(assetName__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass

    image_not_present_id = []

    for asset in setting_assets:
        if not os.path.exists(asset.get_absolute_image_url):
            image_not_present_id.append(asset.id)

    image_present_queryset = list(setting_assets.exclude(id__in=image_not_present_id))
    image_not_present_queryset = list(setting_assets.filter(id__in=image_not_present_id))

    setting_assets = image_not_present_queryset + image_present_queryset
    form = SettingsImagesForm(initial={'theme': theme})

    return render(request, 'pages/theme/settings_assets_list.html',
                  {'setting_assets': setting_assets, 'theme': theme, 'form': form}
                  )


@permission_required("ipad_config.change_settingsimages")
def setting_assets_edit(request, theme_id, asset_id=None):
    # HotelServiceForm
    theme = Theme.objects.get(pk=theme_id)
    setting_asset = SettingsImages.objects.none()
    form = SettingsImagesForm()
    if asset_id:
        setting_asset = SettingsImages.objects.get(pk=asset_id)
        form = SettingsImagesForm(instance=setting_asset)

    if request.POST:
        is_add_action_failed = False
        if asset_id:
            if request.FILES:
                asset_file = MEDIA_ROOT + "/" + theme.path() + "/setting_images/images/" +\
                             str(request.FILES['assetName'].name)
                if os.path.exists(MEDIA_ROOT + "/" + setting_asset.assetName.name):
                    os.remove(MEDIA_ROOT + "/" + setting_asset.assetName.name)
                if os.path.exists(asset_file):
                    os.remove(asset_file)
            form = SettingsImagesForm(request.POST, request.FILES, instance=setting_asset)
        else:
            is_add_action_failed = True
            form = SettingsImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('setting_assets_list', kwargs={'theme_id': theme_id}))
        else:
            setting_assets = theme.settings_images.all()
            setting_assets = paginate(request, setting_assets, 10)
            template = 'pages/theme/settings_assets_list.html' if \
                is_add_action_failed else 'pages/theme/setting_images_form.html'
            return render(request, template,
                          {
                              'form': form,
                              'setting_asset': setting_asset,
                              'setting_assets': setting_assets,
                              'theme': theme,
                              'is_form_failed': is_add_action_failed
                          }
                          )

    return render(request, 'pages/theme/setting_images_form.html',
                  {
                      'form': form,
                      'setting_asset': setting_asset,
                      'theme': theme
                  }
                  )


@permission_required("ipad_config.view_airlinedetail")
def airline_list(request):
    airlines = AirlineDetail.objects.all()
    form = AirlineDetailForm()

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            airlines = airlines.filter(
                Q(airlineName__icontains=search_text) |
                Q(airlineCode__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass

    airlines = paginate(request, airlines, 10)

    return render(request, 'pages/theme/airline_list.html', {
        'airlines': airlines,
        'form': form
    })


@permission_required("ipad_config.change_airlinedetail")
def airline_edit(request, airline_id=None):
    form = AirlineDetailForm()
    airline = None
    if airline_id:
        airline = AirlineDetail.objects.get(pk=airline_id)
        form = AirlineDetailForm(instance=airline)
    is_add_action_failed = False
    if request.POST:
        if airline_id:
            form = AirlineDetailForm(request.POST, instance=airline)
        else:
            is_add_action_failed = True
            form = AirlineDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('airlines', kwargs={}))
        else:
            airlines = AirlineDetail.objects.all()
            airlines = paginate(request, airlines, 10)
            template = 'pages/theme/airline_list.html' if is_add_action_failed else 'pages/theme/airline_form.html'
            return render(request, template, {
                'airlines': airlines,
                'form': form,
                'airline': airline,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/theme/airline_form.html',
                  {
                      'form': form,
                      'airline': airline
                  }
                  )


@permission_required("ipad_config.delete_airlinedetail")
def airline_delete(request, airline_id):
    airline = AirlineDetail.objects.get(pk=airline_id)
    airline.delete()
    return redirect(reverse('airlines', kwargs={}))


@permission_required("ipad_config.view_airportdetail")
def airport_detail_list(request):
    airport_details = AirportDetail.objects.all()
    form = AirportDetailForm(initial={'location': "null"})

    if request.method == "GET":
        try:
            search_text = request.GET['search_text']
            airport_details = airport_details.filter(
                Q(airport_name__icontains=search_text) |
                Q(country__icontains=search_text) |
                Q(city__icontains=search_text) |
                Q(airport_code__icontains=search_text)
            )
        except Exception as e:
            print(str(e))
            pass

    airport_details = paginate(request, airport_details, 10)

    return render(request, 'pages/theme/airport_detail_list.html', {
        'airport_details': airport_details,
        'form': form
    })


@permission_required("ipad_config.change_airportdetail")
def airport_detail_edit(request, airport_id=None):
    form = AirportDetailForm(initial={'location': "null"})
    airport_detail = None
    if airport_id:
        airport_detail = AirportDetail.objects.get(pk=airport_id)
        form = AirportDetailForm(instance=airport_detail)
    is_add_action_failed = False
    if request.POST:
        if airport_id:
            form = AirportDetailForm(request.POST, instance=airport_detail)
        else:
            is_add_action_failed = True
            form = AirportDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('airport_detail_list', kwargs={}))
        else:
            airport_details = AirportDetail.objects.all()
            airport_details = paginate(request, airport_details, 10)
            template = 'pages/theme/airport_detail_list.html' if \
                is_add_action_failed else 'pages/theme/airport_detail_form.html'
            return render(request, template, {
                'airport_details': airport_details,
                'form': form,
                'airport_detail': airport_detail,
                'is_form_failed': is_add_action_failed
            })

    return render(request, 'pages/theme/airport_detail_form.html',
                  {
                      'form': form,
                      'airport_detail': airport_detail
                  }
                  )


@permission_required("ipad_config.delete_airportdetail")
def airport_detail_delete(request, airport_id):
    airport_detail = AirportDetail.objects.get(pk=airport_id)
    airport_detail.delete()
    return redirect(reverse('airport_detail_list', kwargs={}))


@permission_required("ipad_config.add_airportdetail")
def import_airport_details(request):
    if request.method == 'POST' and request.FILES['airport_details_sqlite']:

        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["airport_details_sqlite"].chunks():
                f.write(chunk)

            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "AIRPORT_DETAILS"
            queue.state = "PENDING"
            queue.save()
            upload_task.delay()
        return redirect(reverse('airport_detail_list', kwargs={}))
    return HttpResponse("Method not supported")


@permission_required("ipad_config.add_airlinedetail")
def import_airline_details(request):
    if request.method == 'POST' and request.FILES['airline_details_sqlite']:

        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.FILES["airline_details_sqlite"].chunks():
                f.write(chunk)

            queue = UploadQueue()
            queue.file_path = f.name
            queue.upload_type = "AIRLINE_DETAILS"
            queue.state = "PENDING"
            queue.save()
            upload_task.delay()
        return redirect(reverse('airlines', kwargs={}))
    return HttpResponse("Method not supported")


@permission_required("")
def export_asset_zip(request, theme_id):
    theme = Theme.objects.get(id=theme_id)
    theme_base = MEDIA_ROOT + "/" + theme.path()
    theme_path = theme_base + "/" + "setting_images"
    zip_path = theme_path + ".zip"
    # make zip of above created folder
    shutil.make_archive(theme_path, 'zip', theme_base, "setting_images")

    # response for file to be downloaded
    response = FileResponse(open(zip_path, 'rb'), as_attachment=True)

    # remove zip and folder after download
    if os.path.exists(zip_path):
        os.remove(zip_path)

    # send response
    return response

