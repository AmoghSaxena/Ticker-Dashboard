import json
import datetime
from .models import TickerDetails,Wings,Floors,Keys
from django.core.files.storage import FileSystemStorage

# from .form import logo
# from .form import ImageForm

CONFIG_DATA={
    "static_ticker_condition":False,
    "main_ticker_condition":False,
    "moving_ticker_condition":False,
    "secondary_ticker_enabler":False,
    'emergency_ticker_condition':False,
    "time_interval":0
    }

    

def ImageUploader(filename):
    #This function is used to save image from server to our project's readable location#
    photo = open(filename, 'rb')
    new_photo = open('new-photo.jpg', 'wb')
    data = photo.read()
    new_photo.write(data)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def datagetter(request):

    try:
        tickertype=str()
        '''Static Ticker'''
        static_ticker_condition = request.POST.get('static_ticker_enabler')
        position_static_ticker = request.POST.get('static_position_box')
        static_ticker_bgcolor = request.POST.get('static_background_color')
        static_ticker_logo = request.POST.get('static_ticker_logo')
        static_ticker_message = request.POST.get('static_ticker_msg')
        static_ticker_font_color = request.POST.get('static_font_color')
        static_ticker_font_size = request.POST.get('static_font_size')
        static_ticker_font_type = request.POST.get('static_font_type')


        if request.FILES['static_logo']:
            a=request.FILES['static_logo']
            fss=FileSystemStorage()
            fss.save(a.name,a)
                
        '''Primary Ticker'''
        main_ticker_condition = request.POST.get('primary_ticker_enabler')
        main_ticker_position    = request.POST.get('primary_position_box')
        main_ticker_message    = request.POST.get('primary_ticker_msg')
        main_ticker_logo    = request.POST.get('primary_ticker_logo') 
        main_ticker_logo_position    = request.POST.get('primary_ticker_logo_position')
        main_ticker_font    = request.POST.get('primary_font_type')
        main_ticker_font_size    = request.POST.get('primary_font_size')
        main_ticker_bgcolor    = request.POST.get('primary_background_color') 
        main_ticker_font_color    = request.POST.get('primary_font_color')
        main_ticker_speed    = request.POST.get('primary_ticker_speed')
        main_ticker_motion    = request.POST.get('primary_ticker_motion')


        '''Secondary Ticker'''

        optional_ticker_condition= request.POST.get('secondary_ticker_enabler')
        optional_ticker_position= request.POST.get('secondary_position_box')
        optional_ticker_message= request.POST.get('secondary_ticker_msg')
        optional_ticker_font_color= request.POST.get('secondary_font_color')
        optional_ticker_font= request.POST.get('secondary_font_type')
        optional_ticker_font_size= request.POST.get('secondary_font_size')
        optional_ticker_bgcolor= request.POST.get('secondary_background_color')
        optional_ticker_speed= request.POST.get('secondary_ticker_speed')
        optional_ticker_motion= request.POST.get('secondary_ticker_motion')

        '''Animation Ticker'''

        moving_ticker_condition= request.POST.get('animation_ticker_enabler')
        moving_video= request.POST.get('animation_video')
        moving_ticker_localtion= request.POST.get('animation_position')
        moving_ticker_center_size=request.POST.get('animation_ticker_motion')
        
        '''Emergency Ticker'''
            
        emergency_ticker_condition= request.POST.get('emergency_ticker_enabler')
        emergency_media= request.POST.get('emergency_media')

            
        if  static_ticker_condition=='':
                if len(tickertype)==0:
                    tickertype='Static'
                else:
                    tickertype+=', Static'

                CONFIG_DATA['static_ticker_condition']=True
                CONFIG_DATA['position_static_ticker']=position_static_ticker
                CONFIG_DATA['static_ticker_bgcolor']=hex_to_rgb(static_ticker_bgcolor)
                CONFIG_DATA['static_ticker_font_color']=hex_to_rgb(static_ticker_font_color)
                if static_ticker_logo== None:
                    CONFIG_DATA['static_ticker_logo']=False
                else:
                    CONFIG_DATA['static_ticker_logo']=True
                    # ImageUploader(ticker_logo)
                if static_ticker_font_size == 'X-Large':
                    CONFIG_DATA['static_ticker_font_size'] = 80
                    #CONFIG_DATA['static_ticker_image_size'] = 13.45
                elif static_ticker_font_size == 'Large':
                    CONFIG_DATA['static_ticker_font_size'] = 60
                    #CONFIG_DATA['static_ticker_image_size'] = 15.45
                elif static_ticker_font_size == 'Normal':
                    CONFIG_DATA['static_ticker_font_size'] = 40
                    #CONFIG_DATA['static_ticker_image_size'] = 17.45
                elif static_ticker_font_size == 'Small':
                    CONFIG_DATA['static_ticker_font_size'] = 20
                    #CONFIG_DATA['static_ticker_image_size'] = 19.45
                
                if static_ticker_font_type == 'TimesNewRoman' or static_ticker_font_type == 'MyriadProFont' or static_ticker_font_type == 'Ubuntu':
                    CONFIG_DATA['static_ticker_font'] = static_ticker_font_type
                elif static_ticker_font_type == 'Chinese':
                    CONFIG_DATA['static_ticker_font'] = 'ZCOOLQingKeHuangYou'
                elif static_ticker_font_type == 'Japanese':
                    CONFIG_DATA['static_ticker_font'] = 'NotoSansJP'
                elif static_ticker_font_type == 'Arabic':
                    CONFIG_DATA['static_ticker_font'] = 'NotoSansArabic'
                elif static_ticker_font_type == 'Russian' or static_ticker_font_type == 'Turkish' or static_ticker_font_type == 'Spanish' or static_ticker_font_type == 'Hindi' or static_ticker_font_type == 'French' or static_ticker_font == 'Italian':
                    CONFIG_DATA['font_type'] = 'FreeSans'

                CONFIG_DATA['static_ticker_message']=static_ticker_message

        else:
                CONFIG_DATA['static_ticker_condition']=False
                print('Static condition false')

        '''Secondary Ticker Conditions'''
        if optional_ticker_condition == '':
                if len(tickertype)==0:
                    tickertype='Secondary'
                else:
                    tickertype+=', Secondary'
                CONFIG_DATA['optional_ticker_condition']=True
                CONFIG_DATA['optional_ticker_position'] =optional_ticker_position
                CONFIG_DATA['optional_ticker_message'] = optional_ticker_message
            
                if optional_ticker_font == 'TimesNewRoman' or optional_ticker_font == 'MyriadProFont' or optional_ticker_font == 'Ubuntu':
                    CONFIG_DATA['optional_ticker_font'] = optional_ticker_font
                elif optional_ticker_font == 'Chinese':
                    CONFIG_DATA['optional_ticker_font'] = 'ZCOOLQingKeHuangYou'
                elif optional_ticker_font == 'Japanese':
                    CONFIG_DATA['optional_ticker_font'] = 'NotoSansJP'
                elif optional_ticker_font == 'Arabic':
                    CONFIG_DATA['optional_ticker_font'] = 'NotoSansArabic'
                elif optional_ticker_font == 'Russian' or optional_ticker_font == 'Turkish' or optional_ticker_font == 'Spanish' or optional_ticker_font == 'Hindi' or optional_ticker_font == 'French' or optional_ticker_font == 'Italian':
                    CONFIG_DATA['optional_ticker_font'] = 'FreeSans'
                CONFIG_DATA['optional_ticker_font_size'] = optional_ticker_font_size
                CONFIG_DATA['optional_ticker_bgcolor'] = optional_ticker_bgcolor
                CONFIG_DATA['optional_ticker_font_color'] = hex_to_rgb(optional_ticker_font_color)
                CONFIG_DATA['optional_ticker_speed'] = optional_ticker_speed
                CONFIG_DATA['optional_ticker_motion'] = optional_ticker_motion
                
        else:
                CONFIG_DATA['optional_ticker_condition']=False
            

        '''Primary Ticker'''

        if main_ticker_condition == '':
                if len(tickertype)==0:
                    tickertype='Primary'
                else:
                    tickertype+=', Primary'
                CONFIG_DATA['main_ticker_condition']=True
                CONFIG_DATA['main_ticker_position'] =main_ticker_position
                CONFIG_DATA['main_ticker_message'] = main_ticker_message
                CONFIG_DATA['main_ticker_logo'] = main_ticker_logo
                if CONFIG_DATA['main_ticker_logo'] == 'on':
                    CONFIG_DATA['main_ticker_logo_position'] = main_ticker_logo_position
                    if upload_logo == False:
                        upload_logo = True
            
                if main_ticker_font == 'TimesNewRoman' or main_ticker_font == 'MyriadProFont' or main_ticker_font == 'Ubuntu':
                    CONFIG_DATA['main_ticker_font'] = main_ticker_font
                elif main_ticker_font == 'Chinese':
                    CONFIG_DATA['main_ticker_font'] = 'ZCOOLQingKeHuangYou'
                elif main_ticker_font == 'Japanese':
                    CONFIG_DATA['main_ticker_font'] = 'NotoSansJP'
                elif main_ticker_font == 'Arabic':
                    CONFIG_DATA['main_ticker_font'] = 'NotoSansArabic'
                elif main_ticker_font == 'Russian' or main_ticker_font == 'Turkish' or main_ticker_font == 'Spanish' or main_ticker_font == 'Hindi' or main_ticker_font == 'French' or main_ticker_font == 'Italian':
                    CONFIG_DATA['main_ticker_font'] = 'FreeSans'
                CONFIG_DATA['main_ticker_font_size'] = main_ticker_font_size
                CONFIG_DATA['main_ticker_bgcolor'] = main_ticker_bgcolor
                CONFIG_DATA['main_ticker_font_color'] = hex_to_rgb(main_ticker_font_color)
                CONFIG_DATA['main_ticker_speed'] = main_ticker_speed
                CONFIG_DATA['main_ticker_motion'] = main_ticker_motion
                
        else:
                CONFIG_DATA['main_ticker_condition']=False
            

        '''Animation Ticker'''
        if moving_ticker_condition == '':
                if len(tickertype)==0:
                    tickertype='Animation '
                else:
                    tickertype+=', Animation'
                CONFIG_DATA['moving_ticker_condition']= True
                
                CONFIG_DATA['moving_ticker_localtion'] = moving_ticker_localtion
                if CONFIG_DATA['moving_ticker_localtion'] == "center":
                    CONFIG_DATA['moving_ticker_center_size'] = moving_ticker_center_size
        else:
                CONFIG_DATA['moving_ticker_condition']=False

        '''Emergency Ticker'''

        if emergency_ticker_condition == '':
                if len(tickertype)==0:
                    tickertype='Emergency '
                else:
                    tickertype+=', Emergency'
                CONFIG_DATA['emergency_ticker_condition']=True
        else:
                CONFIG_DATA['emergency_ticker_condition']=False
        
    #     "static_ticker_condition":False,
    # "main_ticker_condition":False,
    # "moving_ticker_condition":False,
    # "secondary_ticker_enabler":False,
    # 'emergency_ticker_condition':False,
    #     if (CONFIG_DATA['static_ticker_condition'] or CONFIG_DATA['main_ticker_condition'] or 
    #        CONFIG_DATA['moving_ticker_condition'] or CONFIG_DATA['secondary_ticker_enabler'] or 
    #        CONFIG_DATA['emergency_ticker_condition'])
    
        CONFIG_DATA['time_interval'] = request.POST.get('time_interval')
        xyz=json.dumps(CONFIG_DATA)
 
        data_saver(tickertype,xyz)

        t=TickerDetails.objects.filter(ticker_type=tickertype).filter(ticker_json=xyz).values()
        # print(t.get())
        return t.get()
    except Exception as e:
        print(e)


def data_saver(tickertype,jsondata):
    tickerobj=TickerDetails()
    tickerobj.ticker_type=tickertype
    tickerobj.ticker_json=jsondata
    # tickerobj.dated_on=datetime.datetime.now()
    tickerobj.is_active=1
    tickerobj.is_deleted=0
    tickerobj.created_on=datetime.datetime.now()
    tickerobj.modified_on=datetime.datetime.now()
    # tickerobj.photo=form
    tickerobj.save()

def schedulingdata():
    fd=Floors.objects.values_list('name')
    wd=Wings.objects.values_list('name')
    kd=Keys.objects.values_list('number')

    f=list()
    w=list()
    k=list()

    for i in fd:
        f.append(i[0])

    for i in wd:
        w.append(i[0])

    for i in kd:
        k.append(i[0])

    scheduledata={
        "floor":f,
        "wings":w,
        "keys":k
    }

    # print(scheduledata)
    return scheduledata

