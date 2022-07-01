TABLE_META = {

    "airlinedetails": {
        "airlineName": "Text",
        "airlineCode": "Text",
        "imageName": "Text",
        "position": "Integer"
    },

    "airportdetails": {
        "airport_name": "Text",
        "airport_code": "Text",
        "country": "Text",
        "city": "Text",
        "city_code": "Text",
        "location": "Text",
        "status": "Integer",
        "position": "Integer"
    },

    "time_zone": {
        "city_id": "Integer",
        "city_name": "Text",
        "country_name": "Text",
        "timezone_id": "Text"
    },

    "currency_types": {
        "currency_name": "Text",
        "currency_code": "Text",
        "position": "Integer",
        "type": "Text",
        "flag_image_name": "Text",
        "locale_identifilre": "Text"
    },

    "weathericon": {
        "weathercode": "Integer",
        "unicode": "Text",
        "iconvault_unicode": "Text",
        "background_image": "Text"
    },

    "color_style_mapping": {
        "color_style_name": "Text",
        "apply_on": "Text",
        "module_name": "Text"
    },

    "font_style_mapping": {
        "font_style_name": "Text",
        "apply_on": "Text",
        "module_name": "Text",
        "state": "Text"
    },

    "color_style": {
        "id": "Integer",
        "color_style_name": "Text",
        "attributes": "Text",
        "lang_code": "Text"
    },

    "font_style": {
        "id": "Integer",
        "font_style_name": "Text",
        "font_name": "Text",
        "font_size": "Real",
        "font_color": "Text",
        "shadow_color": "Text",
        "shadow_offset": "Text",
        "shadow_radius": "Real",
        "shadow_opacity": "Real",
        "attributes": "Text",
        "lang_code": "Text"
    },

    "location_category": {
        "cat_id": "Integer",
        "name": "Text",
        "position": "Integer"
    },

    "location_search": {
        "places": "Text",
        "displayname": "Text",
        "position": "Integer",
        "cat_id": "Integer"
    },

    "hotel_service_mapping": {
        "id": "Integer",
        "type_path": "Text",
        "feature_type": "Text",
        "language_code": "Text"
    },

    "hotel_services": {
        "id": "Integer",
        "name": "Text",
        "image": "Text",
        "feature_type": "Text",
        "position": "Integer",
        "is_active": "Integer"
    },

    "main_features": {
        "id": "Integer",
        "parent_id": "Integer",
        "position": "Integer",
        "enabled": "Integer",
        "name": "Text",
        "feature_images": "Text",
        "feature": "Text",
        "sub_feature": "Text",
        "room_id": "Integer",
        "controller_id": "Integer",
        "contains_subcategory": "Integer",
        "app_version": "Text"
    },

    "splash_images": {
        "image_key": "Text",
        "position": "Integer",
        "visibility": "Integer"
    },
    "common_settings": {
        "key": "Text",
        "value": "Text"
    },
    "home_features": {
        "id": "Integer",
        "enabled": "Integer",
        "name": "Text",
        "image_name": "Text",
        "selected_image_name": "Text",
        "feature": "Text",
        "position": "Integer",
        "command": "Text"
    },
    "features_setting": {
        "id": "Integer",
        "feature_id": "Integer",
        "feature_name": "Text",
        "parameters": "Text"
    },
    "home_services": {
        "id": "Integer",
        "name": "Text",
        "image_name": "Text",
        "selected_image_name": "Text",
        "type": "Text",
        "feature": "Text",
        "size": "Text",
        "command": "Text",
        "position": "Integer",
        "enabled": "Integer",
        "is_evening": "Integer",
        "is_morning": "Integer",
    }

}

EXPORT_TABLES = [
    {
        "table_name": "airlinedetails",
        "model_name": "AirlineDetail",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE airlinedetails ( [airlineName] Text , [airlineCode] Text , [imageName] Text , [position] Integer  );",
        "index_query": ""
    },
    {
        "table_name": "airportdetails",
        "model_name": "AirportDetail",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE airportdetails ( [airport_name] Text , [airport_code] Text , [country] Text , [city] Text , [city_code] Text , [location] Text , [status] Integer , [position] Integer  );",
        "index_query": ""
    },
    {
        "table_name": "time_zone",
        "model_name": "TimeZone",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE time_zone ( [city_id] Integer , [city_name] Text , [country_name] Text , [timezone_id] Text  );",
        "index_query": ""
    },
    {
        "table_name": "currency_types",
        "model_name": "CurrencyTypes",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE currency_types ( [currency_name] Text , [currency_code] Text , [position] Integer , [type] Text , [flag_image_name] Text , [locale_identifilre] Text  );",
        "index_query": ""
    },
    {
        "table_name": "weathericon",
        "model_name": "Weathericon",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE weathericon ( [weathercode] Integer , [unicode] Text , [iconvault_unicode] Text , [background_image] Text  );",
        "index_query": ""
    },
    {
        "table_name": "color_style_mapping",
        "model_name": "ColorStyleMapping",
        "filter": False,
        "isTheme": True,
        "create_table_sql": '''CREATE TABLE color_style_mapping (
             [color_style_name] Text , [apply_on] Text , [module_name] Text,
             FOREIGN KEY ("color_style_name") REFERENCES "color_style" ("color_style_name") ON DELETE RESTRICT ON UPDATE RESTRICT
             )
        ''',
        "index_query": ""
    },
    {
        "table_name": "color_style",
        "model_name": "ColorStyle",
        "filter": False,
        "isTheme": True,
        "create_table_sql": '''
            CREATE TABLE "color_style" (
            "id" integer NOT NULL DEFAULT '0' PRIMARY KEY AUTOINCREMENT,
            "color_style_name" text NOT NULL,
            "attributes" text NULL, "lang_code" text DEFAULT 'en');
        ''',
        "index_query": "CREATE UNIQUE INDEX 'color_style_mapping_apply_on_module_name' ON 'color_style_mapping' ('apply_on', 'module_name');"
    },
    {
        "table_name": "font_style",
        "model_name": "FontStyle",
        "filter": False,
        "isTheme": True,
        "create_table_sql": '''CREATE TABLE font_style (
            [id] Integer ,
            [font_style_name] Text ,
            [font_name] Text ,
            [font_size] Real ,
            [font_color] Text ,
            [shadow_color] Text ,
            [shadow_offset] Text ,
            [shadow_radius] Real ,
            [shadow_opacity] Real ,
            [attributes] text NULL,
            [lang_code] text DEFAULT 'en'
        );''',
        "index_query": ""
    },
    {
        "table_name": "font_style_mapping",
        "model_name": "FontStyleMapping",
        "filter": False,
        "isTheme": True,
        "create_table_sql": '''CREATE TABLE font_style_mapping (
             [font_style_name] Text , [apply_on] Text , [module_name] Text , [state] Text,
             FOREIGN KEY ("font_style_name") REFERENCES "font_style" ("font_style_name") ON DELETE RESTRICT ON UPDATE RESTRICT
        );''',
        "index_query": ""
    },
    {
        "table_name": "location_category",
        "model_name": "LocationCategory",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE location_category ( [cat_id] Integer , [name] Text , [position] Integer  );",
        "index_query": ""
    },
    {
        "table_name": "location_search",
        "model_name": "LocationSearch",
        "filter": False,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE location_search ( [places] Text , [displayname] Text , [position] Integer , [cat_id] Integer  );",
        "index_query": ""
    },
    {
        "table_name": "hotel_service_mapping",
        "model_name": "HotelServiceMapping",
        "filter": True,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE hotel_service_mapping ([id] Integer, [type_path] Text , [feature_type] Text , [language_code] Text  );",
        "index_query": ""
    },
    {
        "table_name": "hotel_services",
        "model_name": "HotelServices",
        "filter": True,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE hotel_services ([id] Integer, [name] Text , [image] Text , [feature_type] Text , [position] Integer , [is_active] Integer  );",
        "index_query": ""
    },
    {
        "table_name": "main_features",
        "model_name": "MainFeatures",
        "filter": True,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE main_features ( [id] Integer , [parent_id] Integer , [position] Integer , [enabled] Integer , [name] Text , [feature_images] Text , [feature] Text , [sub_feature] Text , [room_id] Integer , [controller_id] Integer , [contains_subcategory] Integer , [app_version] Text  );",
        "index_query": ""
    },
    {
        "table_name": "splash_images",
        "model_name": "SplashImages",
        "filter": True,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE splash_images ( [image_key] Text , [position] Integer , [visibility] Integer  );",
        "index_query": ""
    },
    {
        "table_name": "home_features",
        "model_name": "HomeFeatures",
        "filter": True,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE home_features ( [id] Integer , [enabled] Integer , [name] Text , [image_name] Text , [selected_image_name] Text , [feature] Text , [position] Integer , [command] Text  );",
        "index_query": ""
    },
    {
        "table_name": "common_settings",
        "model_name": "CommonSettings",
        "filter": True,
        "isTheme": False,
        "create_table_sql": "CREATE TABLE common_settings ( [key] Text , [value] Text  );",
        "index_query": ""
    },
    {
        "table_name": "features_setting",
        "model_name": "FeaturesSetting",
        "filter": True,
        "isTheme": False,
        "create_table_sql": '''
            CREATE TABLE "features_setting" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "feature_id" integer NOT NULL DEFAULT '',
            "feature_name" text NOT NULL,
            "parameters" text,
            FOREIGN KEY ("feature_id") REFERENCES "main_features" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT
            );
        ''',
        "index_query": "CREATE UNIQUE INDEX 'features_setting_feature_id' ON 'features_setting' ('feature_id');"
    },
    {
        "table_name": "home_services",
        "model_name": "DVHomeService",
        "filter": True,
        "isTheme": False,
        "create_table_sql": '''
            CREATE TABLE "home_services" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" text NOT NULL,
            "image_name" text NOT NULL,
            "selected_image_name" text NOT NULL,
            "type" text NOT NULL,
            "feature" text NOT NULL,
            "size" text NOT NULL,
            "command" text NULL,
            "position" integer NOT NULL,
            "enabled" integer NOT NULL
            , "is_evening" integer NULL, "is_morning" integer NULL)
        ''',
        "index_query": ""
    }
]

LANG_EXPORT_TABLES = [
    {
        "table_name": "dv_language",
        "model_name": "DVLanguage",
        "filter": False,
        "create_table_sql": '''CREATE TABLE "dv_language" (
            "tag" text NULL,
            "field" text NULL,
            "lang_code" text NULL,
            "module_name" text NULL DEFAULT ''
            )
        ''',
        "index_query": ""
    },
    {
        "table_name": "dv_language_code",
        "model_name": "DVLanguageCode",
        "filter": False,
        "create_table_sql": '''
            CREATE TABLE "dv_language_code" (
            "lang_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "lang_code" text NULL,
            "display_name" text NULL,
            "position" integer NULL,
            "is_active" integer NOT NULL DEFAULT '1',
            "image" text NULL
            )
        ''',
        "index_query": ""
    }
    # {
    #     "table_name": "sqlite_sequence",
    #     "model_name":"LanguageSqliteSequence",
    #     "filter": False,
    #     "create_table_sql": "CREATE TABLE sqlite_sequence(name varchar(255), seq int)",
    #     "index_query": ""
    # }
]

LANG_TABLE_META = {
    "dv_language": {
        "tag": "Text",
        "field": "Text",
        "lang_code": "Text",
        "module_name": "Text"
    },
    "dv_language_code": {
        "lang_id": "Text",
        "lang_code": "Text",
        "display_name": "Text",
        "position": "Integer",
        "is_active": "Integer",
        "image": "Text"
    }
    # "sqlite_sequence" : {
    #     "name": "Text",
    #     "seq": "Integer"
    # },

}

HOME_SERVICES_SEED = [
    {
        "id": "1",
        "name": "ROOM TEMPERATURE",
        "image_name": "ac2.png",
        "selected_image_name": "ac2-sel.png",
        "type": "with_image",
        "feature": "temperature",
        "size": "{180,270}",
        "command": "ac",
        "position": "1",
        "enabled": "1",
        "is_evening": "1",
        "is_morning": "1"
    },
    {
        "id": "2",
        "name": "DND",
        "image_name": "dnd2.png",
        "selected_image_name": "dnd2-sel.png",
        "type": "with_image",
        "feature": "dnd",
        "size": "{180,123}",
        "command": "dnd",
        "position": "2",
        "enabled": "1",
        "is_evening": "1",
        "is_morning": "0"
    },
    {
        "id": "3",
        "name": "Clean My Room",
        "image_name": "mur2.png",
        "selected_image_name": "mur2-sel.png",
        "type": "with_image",
        "feature": "mur",
        "size": "{180,123}",
        "command": "mur",
        "position": "3",
        "enabled": "0",
        "is_evening": "0",
        "is_morning": "0"
    },
    {
        "id": "4",
        "name": "Clear Tray",
        "image_name": "tray2.png",
        "selected_image_name": "tray-sel.png",
        "type": "with_image",
        "feature": "cleartray",
        "size": "{180,123}",
        "command": "tray",
        "position": "4",
        "enabled": "0",
        "is_evening": "1",
        "is_morning": "0"
    },
    {
        "id": "5",
        "name": "Sleep",
        "image_name": "sleep2_disable.png",
        "selected_image_name": "sleep-sel.png",
        "type": "with_image",
        "feature": "scene",
        "size": "{180,123}",
        "command": "light8",
        "position": "5",
        "enabled": "1",
        "is_evening": "1",
        "is_morning": "0"
    },
    {
        "id": "6",
        "name": "Play Spotify",
        "image_name": "spotify2.png",
        "selected_image_name": "spotify2-sel.png",
        "type": "with_image",
        "feature": "spotify",
        "size": "{180,270}",
        "command": "spotify",
        "position": "6",
        "enabled": "1",
        "is_evening": "1",
        "is_morning": "1"
    },
    {
        "id": "7",
        "name": "Preorder Your Breakfast",
        "image_name": "breakfast2.png",
        "selected_image_name": "breakfast2-sel.png",
        "type": "with_image",
        "feature": "breakfast",
        "size": "{180,270}",
        "command": "breakfast",
        "position": "7",
        "enabled": "1",
        "is_evening": "1",
        "is_morning": "0"
    },
    {
        "id": "8",
        "name": "Disney",
        "image_name": "disney2.png",
        "selected_image_name": "disney2-sel.png",
        "type": "with_image",
        "feature": "disneyplus",
        "size": "{180,270}",
        "command": "disney",
        "position": "8",
        "enabled": "0",
        "is_evening": "1",
        "is_morning": "1"
    },
    {
        "id": "9",
        "name": "Luggage Assistance",
        "image_name": "dnd2.png",
        "selected_image_name": "dnd2-sel.png",
        "type": "with_image",
        "feature": "luggage",
        "size": "{180,123}",
        "command": "luggage",
        "position": "2",
        "enabled": "1",
        "is_evening": "0",
        "is_morning": "1"
    },
    {
        "id": "10",
        "name": "Airport      Transfer",
        "image_name": "Airport.png",
        "selected_image_name": "Airport-sel.png",
        "type": "with_image",
        "feature": "airport",
        "size": "{180,123}",
        "command": "airport",
        "position": "3",
        "enabled": "1",
        "is_evening": "0",
        "is_morning": "1"
    },
    {
        "id": "11",
        "name": "Request For Late Checkout",
        "image_name": "checkout_disable.png",
        "selected_image_name": "checkout-sel.png",
        "type": "with_image",
        "feature": "late_checkout",
        "size": "{180,270}",
        "command": "checkout",
        "position": "5",
        "enabled": "1",
        "is_evening": "0",
        "is_morning": "1"
    },
    {
        "id": "12",
        "name": "Book a Sunday Brunch",
        "image_name": "breakfast2.png",
        "selected_image_name": "breakfast2-sel.png",
        "type": "with_image",
        "feature": "brunch",
        "size": "{180,270}",
        "command": "brunch",
        "position": "8",
        "enabled": "1",
        "is_evening": "0",
        "is_morning": "1"
    }
]
