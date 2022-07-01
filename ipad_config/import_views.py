# Python Imports
import tempfile
import json

# Django Imports
from django.shortcuts import redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Project Imports
from .models import Hotel, JavaConfig, DVHomeService, JavaConfigChanges
from .table_meta import HOME_SERVICES_SEED


# upload java config function
def upload_java_configs(hotel, file_path, request):
    json_data = open(file_path, 'r')
    data1 = json.load(json_data)

    for obj in data1:
        if not JavaConfig.objects.filter(config_key=obj["config_key"], related_hotel=hotel,
                                         module=obj["module"]).exists():
            obj.pop("config_id")
            obj.pop("modified_by")
            obj.pop("modified_on")
            obj.pop("created_on")
            obj.pop("hotel_id")
            config = JavaConfig(**obj)
            config.related_hotel = hotel
            config.hotel_id = hotel.hotel_id
            config.save()
            JavaConfigChanges.objects.create(hotel=hotel, java_config=config, config_key=config.config_key,
                                             module=config.module, config_val=config.config_val, added_by=request.user)

        else:
            config = JavaConfig.objects.filter(config_key=obj["config_key"], related_hotel=hotel,
                                               module=obj["module"]).first()
            if config.config_val != obj["config_val"] or config.val_type != obj["val_type"] or \
                config.description != obj["description"] or config.is_deletable != obj["is_deletable"] or \
                config.is_active != obj["is_active"] or config.delete_msg != obj["delete_msg"] or \
                config.is_deleted != obj["is_deleted"] or config.created_by != obj["created_by"]:
                config.config_val = obj["config_val"]
                config.val_type = obj["val_type"]
                config.description = obj["description"]
                config.is_deletable = obj["is_deletable"]
                config.is_active = obj["is_active"]
                config.delete_msg = obj["delete_msg"]
                config.is_deleted = obj["is_deleted"]
                config.created_by = obj["created_by"]

                config.save()

                JavaConfigChanges.objects.create(hotel=hotel, java_config=config, config_key=config.config_key,
                                                 module=config.module, config_val=config.config_val,
                                                 added_by=request.user)

    json_data.close()


def import_java_config_json(request):
    if request.method == 'POST' and request.FILES['java_cofig_json']:
        hotel_id = request.POST['hotel']
        hotel = Hotel.objects.get(pk=hotel_id)

        with tempfile.NamedTemporaryFile() as f:
            for chunk in request.FILES["java_cofig_json"].chunks():
                f.write(chunk)

            upload_java_configs(hotel, f.name, request)
        return redirect(reverse('java_configs_list', kwargs={'hotel_id': hotel.id}))


def import_home_service_defaults(request, hotel_id):
    try:
        hotel = Hotel.objects.get(pk=hotel_id)
        for obj in HOME_SERVICES_SEED:
            obj.pop("id")
            try:
                home_service = DVHomeService(**obj)
                home_service.hotel = hotel
                home_service.save()
            except Exception as e:
                print(e)
    except ObjectDoesNotExist as e:
        print(str(e))
        return HttpResponse("Hotel not found")

    return HttpResponse("Ok")
