# python imports
import json

# django imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# project imports
from .models import MainFeatures


def create_main_feature(room_type):
    json_data = open('ipad_config/features.json', 'r')
    data = json.load(json_data)
    position = 1
    for item in data:
        feature_name = item['name']
        feature = MainFeatures(room_type=room_type, name=feature_name, position=position)
        feature.save()
        position += 1
    json_data.close()


def paginate(request, items, data_count):
    page = request.GET.get('page', 1)
    paginator = Paginator(items, data_count)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items
