# Python Imports
import shutil
import os
import json
import sqlite3
from itertools import chain

# Django Imports
from django.forms.models import model_to_dict
from django.db import connections
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

# Projects Imports
from .models import RoomType, HotelAirportDetail, DVHotelLanguage, DVHotelLanguageCode, FQDN, \
    IpadConfigChanges
from .table_meta import TABLE_META, EXPORT_TABLES, LANG_EXPORT_TABLES, LANG_TABLE_META
from config.settings.base import MEDIA_URL, ASSET_LOCATION, CLOUD_URL, APPS_DIR

"""
settings.sqlite export
"""


def save_changed_tables(path, queue, type):
    if type == "image":
        with open(path + '/assets.json') as f:
            a = json.load(f)

        if not os.path.exists(path + "/assets_copy.json".format(type)):
            for dct in a["ipad"]:
                name = dct["assetName"].split("/").pop()
                link = dct["cloud_link"]
                IpadConfigChanges.objects.create(queue=queue, action="added", type=type, name=name, table=link)
            return

        with open(path + '/assets_copy.json') as f:
            b = json.load(f)

        added = [[i["assetName"].split("/").pop(), i["cloud_link"]] for i in a["ipad"] if i not in b["ipad"]]
        deleted = [[i["assetName"].split("/").pop(), i["cloud_link"]] for i in b["ipad"] if i not in a["ipad"]]

        for name, link in added:
            IpadConfigChanges.objects.create(queue=queue, action="added", type=type, name=name, table=link)
        for name, link in deleted:
            IpadConfigChanges.objects.create(queue=queue, action="deleted", type=type, name=name, table=link)
        os.remove(path + "/assets_copy.json")
        return

    else:

        if not os.path.exists(path + "/{}_copy.sqlite".format(type)):
            open(os.path.join(path, "{}_copy.sqlite".format(type)), "+w")

        c1 = sqlite3.connect(path + '/{}.sqlite'.format(type)).cursor()
        c2 = sqlite3.connect(path + '/{}_copy.sqlite'.format(type)).cursor()

        tables1 = set(list(chain(*c1.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())))
        tables2 = set(list(chain(*c2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())))

        for name in list(tables1 - tables2):
            IpadConfigChanges.objects.create(queue=queue, action="added", type=type, name=name)
        for name in list(tables2 - tables1):
            IpadConfigChanges.objects.create(queue=queue, action="deleted", type=type, name=name)

        for name in list(tables1 & tables2):
            data1 = set([row for row in c1.execute("SELECT * FROM {}".format(name)).fetchall()])
            data2 = set([row for row in c2.execute("SELECT * FROM {}".format(name)).fetchall()])

            for added in list(set().union(data1 - data2)):
                IpadConfigChanges.objects.create(queue=queue, action="added", type=type, name=added, table=name)
            for deleted in list(set().union(data2 - data1)):
                IpadConfigChanges.objects.create(queue=queue, action="deleted", type=type, name=deleted, table=name)

        os.remove(path + "/{}_copy.sqlite".format(type))
        c1.close()
        return


def get_values(result, fields, table_name, model, room_type):
    item_dict = model_to_dict(result)
    values = ""
    last_value = len(fields.keys()) - 1
    for index, key in enumerate(fields.keys()):
        if table_name == 'main_features' and key == 'feature_images':
            value = json.dumps(model.objects.get(pk=item_dict['main_feature_id'], room_type=room_type).feature_images)
        elif table_name == 'main_features' and key == 'id':
            value = str(item_dict['main_feature_id'])
        elif table_name == 'main_features' and key == 'parent_id':
            value = str(item_dict['parent_id'])
        elif table_name == 'common_settings' and key == 'value':
            value = json.dumps(model.objects.get(id=item_dict['id'], room_type=room_type).value)
        elif table_name == 'features_setting' and key == 'feature_id':
            value = str(item_dict['main_feature'])
        elif table_name == 'features_setting' and key == 'id':
            value = str(item_dict['feature_settings_id'])
        elif table_name == 'hotel_services' and key == 'image':
            value = model.objects.get(id=item_dict['id'], room_type=room_type).image
        else:
            value = str(item_dict[key])
        value = value.replace("'", "''")

        if value == 'None':
            value = 'Null'

        if len(value) <= 0:
            value = 'Null'

        if value == 'Null':
            if table_name == 'font_style':  # Font style null handling
                values += "''"
            elif table_name == 'main_features' and key == 'parent_id':
                values += "'0'"
            else:
                values += " NULL "
        else:
            values += "'" + value + "'"

        if not index == last_value:
            values += ", "
    return values


def export_sqlite(path, type, queue):
    try:
        if os.path.exists(path + "/settings.sqlite"):
            shutil.copy(path + "/settings.sqlite", path + "/settings_copy.sqlite")
        # Creating sqlite
        sqlite_file = open(os.path.join(path, "settings.sqlite"), "+w")
        conn = sqlite3.connect(sqlite_file.name)
        c = conn.cursor()
        connections['mycon'] = conn

        # creating table and inserting data
        room_type = RoomType.objects.get(name=type.name, hotel=type.hotel)
        for item in EXPORT_TABLES:
            model_name = item['model_name']
            table_name = item['table_name']
            is_filter = item['filter']
            is_theme_table = item['isTheme']
            model = apps.get_model('ipad_config', model_name)
            fields = TABLE_META[table_name]
            column_names = []

            for index, field_name in enumerate(fields.keys()):
                column_names.append(field_name)
            query = item['create_table_sql']  # Direct Query
            c.execute(query)

            if len(item['index_query']) > 0:
                c.execute(item['index_query'])

            # Tables created End

            columns = ", ".join(column_names)
            insert_query = "INSERT INTO {0} ({1}) VALUES ".format(table_name, columns)

            # filtering data if filter is present
            if is_filter:
                if model_name == "HotelServiceMapping":
                    results = model.objects.filter(id__room_type=room_type)
                elif model_name in ["SplashImages", "DVHomeService"]:
                    results = model.objects.filter(hotel=room_type.hotel)
                else:
                    results = model.objects.filter(room_type=room_type)
            elif is_theme_table:
                theme = room_type.theme
                results = model.objects.filter(theme=theme)
            else:
                results = model.objects.all()  # (room_type=type)

            if model_name == "CommonSettings":
                results = results.filter(parent=None)

            if model_name == "ColorStyleMapping":
                results = list(chain(list(results.exclude(module_name__isnull=False)),
                                     list(results.exclude(module_name__isnull=True))))

            if len(results) > 0:
                last_row = len(results) - 1
                for result in results:
                    values = get_values(result, fields, table_name, model, room_type)
                    if last_row == 0:
                        this_query = "({0}) ".format(values)
                    else:
                        this_query = "({0}), ".format(values)
                    last_row -= 1

                    insert_query += this_query

                c.execute(insert_query)
            conn.commit()
            if table_name == 'airportdetails':
                for airport in HotelAirportDetail.objects.filter(hotel=type.hotel):
                    sel_query = "select airport_name,airport_code from " + table_name + \
                                " where airport_name=? and airport_code=?"
                    c.execute(sel_query, (airport.airport.airport_name, airport.airport.airport_code))
                    rows = c.fetchall()

                    for row in rows:
                        update_query = "Update " + table_name + " set status='" + str(
                            airport.status) + "', position='" + str(airport.position) + "' where airport_name='" + row[
                                           0] + "' and airport_code='" + row[1] + "'"

                        c.execute(update_query)
                        conn.commit()
        sqlite_file.flush()
        sqlite_file.close()

        save_changed_tables(path, queue, type="settings")

        print("file exported")
        return
    except Exception as e:
        print(e)
        raise


"""
language.sqlite export
"""


def get_values_from_model_dict(fields, result):
    item_dict = model_to_dict(result)
    values = ""
    last_value = len(fields.keys()) - 1
    for index, key in enumerate(fields.keys()):
        value = str(item_dict[key])
        value = value.replace("'", "''")

        if value == 'None':
            value = 'Null'

        if len(value) <= 0:
            value = 'Null'

        if value == 'Null':
            values += " NULL "
        else:
            values += "'" + value + "'"

        if not index == last_value:
            values += ", "
    return values


def export_language_sqlite(path, type, queue):
    try:
        if os.path.exists(path + "/language.sqlite"):
            shutil.copy(path + "/language.sqlite", path + "/language_copy.sqlite")
        sqlite_file = open(os.path.join(path, "language.sqlite"), "+w")
        conn = sqlite3.connect(sqlite_file.name)
        c = conn.cursor()
        connections['mycon'] = conn

        for item in LANG_EXPORT_TABLES:
            model_name = item['model_name']
            table_name = item['table_name']
            is_filter = item['filter']
            model = apps.get_model('ipad_config', model_name)
            fields = LANG_TABLE_META[table_name]
            column_names = []

            for index, field_name in enumerate(fields.keys()):
                column_names.append(field_name)
            query = item['create_table_sql']  # Direct Query
            c.execute(query)

            if len(item['index_query']) > 0:
                c.execute(item['index_query'])

            # Tables created End

            columns = ", ".join(column_names)
            insert_query = "INSERT INTO {0} ({1}) VALUES ".format(table_name, columns)

            if is_filter:
                room_type = RoomType.objects.get(name=type)
                results = model.objects.filter(hotel=room_type.hotel)
            else:
                results = model.objects.all()  # (room_type=type)

            if len(results) > 0:
                last_row = len(results) - 1
                for result in results:
                    values = get_values_from_model_dict(fields, result)

                    if last_row == 0:
                        this_query = "({0}) ".format(values)
                    else:
                        this_query = "({0}), ".format(values)
                    last_row -= 1

                    insert_query += this_query
                c.execute(insert_query)
            conn.commit()
            if table_name == 'dv_language':
                for language in DVHotelLanguage.objects.filter(hotel=type.hotel):
                    try:
                        if len(language.module_name) > 0:
                            sel_query = "select tag,lang_code from " + table_name + \
                                        " where tag=? and lang_code=? and module_name=?"
                            c.execute(sel_query, (language.tag, language.lang_code, language.module_name))
                        else:
                            sel_query = "select tag,lang_code from " + table_name + " where tag=? and lang_code=?"
                            c.execute(sel_query, (language.tag, language.lang_code))
                    except Exception as e:
                        print(e)
                        sel_query = "select tag,lang_code from " + table_name + " where tag=? and lang_code=?"
                        c.execute(sel_query, (language.tag, language.lang_code))
                    rows = c.fetchall()

                    if len(rows) < 1:
                        insert_query = "INSERT INTO {0} ({1}) VALUES ".format(table_name, columns)
                        values = get_values_from_model_dict(fields, language)
                        insert_query += "({0}) ".format(values)
                        c.execute(insert_query)
                        conn.commit()
                    else:
                        for row in rows:
                            update_query = "Update " + table_name + " set field='" + language.field + \
                                           "' where tag='" + row[0] + "' and lang_code='" + row[1] + "'"

                            c.execute(update_query)
                            conn.commit()
            elif table_name == 'dv_language_code':
                for hotel_language_code in DVHotelLanguageCode.objects.filter(hotel=type.hotel):
                    sel_query = "select lang_id from " + table_name + " where  lang_id=?"
                    c.execute(sel_query, (hotel_language_code.language_code.lang_id,))
                    rows = c.fetchall()

                    for row in rows:
                        update_query = "Update " + table_name + " set is_active='" + str(
                            hotel_language_code.is_active) + "', position='" + str(
                            hotel_language_code.position) + "' where lang_id='" + str(row[0]) + "'"

                        c.execute(update_query)
                        conn.commit()

        save_changed_tables(path, queue, type="language")
        sqlite_file.flush()
        sqlite_file.close()
        print("file exported")
        return
    except Exception as e:
        print(e)
        raise


"""
asset.json export
"""


def get_asset_obj(s, room):
    obj = {'assetType': s.assetType, 'assetTimestamp': str(int(s.assetTimestamp))}
    url = s.assetName.url
    url = url.replace("%20", " ")
    if os.path.isfile(str(APPS_DIR) + url):
        try:
            asset_image_name = url.split('/')
            asset_image_name = asset_image_name[len(asset_image_name) - 1]
            obj['cloud_link'] = CLOUD_URL + url
            his = FQDN.objects.get(server="HIS", hotel=room.hotel)
            obj['assetName'] = "https://" + his.fqdn.strip() + MEDIA_URL + ASSET_LOCATION + asset_image_name
        except ObjectDoesNotExist:
            obj['assetName'] = url
        return obj
    else:
        return None


def export_assest_json(path, room, queue):
    try:
        if os.path.exists(path + "/assets.json"):
            shutil.copy(path + "/assets.json", path + "/assets_copy.json")
        asset_file = open(os.path.join(path, "assets.json"), "+w")

        ipad = []
        settings_images = room.theme.settings_images.all().distinct('assetName')
        for s in settings_images:
            obj = get_asset_obj(s, room)
            if obj:
                ipad.append(obj)
        for hotel_image in room.hotel.hotel_images.all():
            obj = get_asset_obj(hotel_image, room)
            if obj:
                found = False
                for i in ipad:
                    if obj["assetName"] == i["assetName"]:
                        i["cloud_link"] = obj["cloud_link"]
                        found = True
                        break
                if not found:
                    ipad.append(obj)

        data = json.dumps({"ipad": ipad})
        asset_file.write(data)
        save_changed_tables(path, queue, type="image")
        asset_file.flush()
        asset_file.close()
        return
    except Exception as e:
        print(e)
        raise
