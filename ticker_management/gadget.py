import json
from datetime import datetime,timedelta
import os
from .models import TickerDetails,SetUp
from ticker_management.ticker_schedules import schedulingticker
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree


import logging
logger=logging.getLogger('dashboardLogs')

def dateformatter(dateObj,timeorday):
    dateObj=datetime.strptime(dateObj,"%Y-%m-%dT%H:%M")
    if timeorday=='time':
        # print(dateObj.strftime('%Y-%m-%d %H:%M:%S'))
        return dateObj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return dateObj.strftime('%A')

def FileUploader(request,ticker_db_data):
    dvs_data=SetUp.objects.filter(id=1).values()
    apache_server_url=str(dvs_data.get().get('Apache_server_url'))

    ticker_id=ticker_db_data.get('ticker_id',-1)
    
    temp=ticker_db_data.get('ticker_json',None)

    ticker_json=json.loads(temp)

    fss=FileSystemStorage()

    # print("outside")

    if ticker_json.get('main_ticker_condition','not found')==True and ticker_json.get('main_ticker_logo','not found')==True:

        a=request.FILES['primaryTickerLogo']

        fss.save(a.name,a)
        
        ext=a.name.split('.')[-1]
        filename="%s_%s_%s.%s"%('image',ticker_id,1,ext)

        old_name="{0}{1}{2}".format(fss.base_location,os.sep,a.name)
        new_name="{0}{1}{2}".format(fss.base_location,os.sep,filename)

        os.rename(old_name,new_name)

        ticker_json['main_ticker_logo_name']=apache_server_url+'/'+filename
    
    elif ticker_json.get('static_ticker_condition','not found')==True and ticker_json.get('static_ticker_logo','not found')==True:

        a=request.FILES.get('staticTickerLogo')

        fss.save(a.name,a)

        ext=a.name.split('.')[-1]
        filename="%s_%s_%s.%s"%('image',ticker_id,3,ext)

        old_name="{0}{1}{2}".format(fss.base_location,os.sep,a.name)
        new_name="{0}{1}{2}".format(fss.base_location,os.sep,filename)

        os.rename(old_name,new_name)

        ticker_json['static_ticker_logo_name']=apache_server_url+'/'+filename
    
    elif ticker_json.get('moving_ticker_condition','not found')==True:
        
        a=request.FILES.get('dynamicTickerVideo')

        fss.save(a.name,a)

        ext=a.name.split('.')[-1]
        filename="%s_%s_%s.%s"%('video',ticker_id,4,ext)

        old_name="{0}{1}{2}".format(fss.base_location,os.sep,a.name)
        new_name="{0}{1}{2}".format(fss.base_location,os.sep,filename)

        os.rename(old_name,new_name)

        ticker_json['moving_ticker_logo_name']=apache_server_url+'/'+filename

    elif  ticker_json.get('emergency_ticker_condition','not found')==True and request.POST.get('emergencySelecter')=='Custom':
        
        a=request.FILES.get('emergencyTickerFile')

        fss.save(a.name,a)

        ext=a.name.split('.')[-1]

        filename=str()

        if ext == 'mp4':
            ticker_json['emergency_ticker_style'] = 'dynamic'
            filename="%s_%s_%s.%s"%('video',ticker_id,5,ext)        
        else:
            ticker_json['emergency_ticker_style'] = 'static'
            filename="%s_%s_%s.%s"%('image',ticker_id,5,ext)
        
        old_name="{0}{1}{2}".format(fss.base_location,os.sep,a.name)
        new_name="{0}{1}{2}".format(fss.base_location,os.sep,filename)
        os.rename(old_name,new_name)

        ticker_json['emergency_ticker_logo_name']=apache_server_url+'/'+filename
    
    else:
        logger.info('No Image for upload')
    
    ticker_json['ticker_id'] = ticker_id
    
    return json.dumps(ticker_json, indent=3)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def datagetter(request):

    CONFIG_DATA={
        "static_ticker_condition":False,
        "main_ticker_condition":False,
        "moving_ticker_condition":False,
        "optional_ticker_condition":False,
        'emergency_ticker_condition':False,
        "time_interval":0
        }
    tickertype=str()
    tickerTitle=str()
    tickerPriority=str()

    try:
        tickerSelection=request.POST.get('tickerSelecter')

        if tickerSelection == 'scrolling':

            tickertype='Scrolling Ticker'
            tickerTitle=request.POST.get('scrollingTickerTitle')
            tickerPriority=request.POST.get('scrollingTickerPriority')

            if request.POST.get('scrollingTickerPriority')=="Emergency":
                CONFIG_DATA['time_interval']= int(864000)
            else:
                CONFIG_DATA['time_interval']= int(request.POST.get('scrollingTickerTimeInterval')) * 60
            
            main_ticker_condition = request.POST.get('primaryScrollingTicker')

            if main_ticker_condition == 'enabled':
        
                try:
                    '''Primary Ticker'''
                    main_ticker_position    = request.POST.get('primaryPositionBox')
                    main_ticker_message    = request.POST.get('primaryTickerMessage')
                    main_ticker_logo    = request.POST.get('primaryTickerLogoEnabler')
                    main_ticker_logo_position    = request.POST.get('primaryTickerLogoPosition')
                    main_ticker_font    = request.POST.get('primaryFontType')
                    main_ticker_font_size    = request.POST.get('primaryFontSize')
                    main_ticker_bgcolor    = request.POST.get('primaryBgColor') 
                    main_ticker_font_color    = request.POST.get('primaryFontColor')
                    main_ticker_speed    = request.POST.get('primaryTickerSpeed')
                    main_ticker_motion    = request.POST.get('primaryTickerMotion')

                    CONFIG_DATA['main_ticker_condition']=True
                    CONFIG_DATA['main_ticker_position'] =main_ticker_position
                    CONFIG_DATA['main_ticker_message'] = main_ticker_message
                    if main_ticker_logo == "enabled":
                        CONFIG_DATA['main_ticker_logo'] = True
                    else:
                        CONFIG_DATA['main_ticker_logo'] = False
                    if CONFIG_DATA['main_ticker_logo'] == True:
                        CONFIG_DATA['main_ticker_logo_position'] = main_ticker_logo_position
                        
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
                    CONFIG_DATA['main_ticker_bgcolor'] = hex_to_rgb(main_ticker_bgcolor)
                    CONFIG_DATA['main_ticker_font_color'] = hex_to_rgb(main_ticker_font_color)
                    CONFIG_DATA['main_ticker_speed'] = main_ticker_speed
                    CONFIG_DATA['main_ticker_motion'] = main_ticker_motion 

                except Exception as primaryscroll:
                    logger.warning('Exception raised during primaryscroll'+primaryscroll)
            
            optional_ticker_condition= request.POST.get('secondaryScrollingEnable')

            if optional_ticker_condition == 'enabled':
                try:
                    '''Secondary Ticker'''
                    optional_ticker_position= request.POST.get('secondaryPositionBox')
                    optional_ticker_message= request.POST.get('secondaryTickerMessage')
                    optional_ticker_font_color= request.POST.get('secondaryFontColor')
                    optional_ticker_font= request.POST.get('secondaryFontType')
                    # optional_ticker_font_size= request.POST.get('secondary_font_size')
                    optional_ticker_bgcolor= request.POST.get('secondaryBgColor')
                    optional_ticker_speed= request.POST.get('secondaryTickerSpeed')
                    optional_ticker_motion= request.POST.get('secondaryTickerMotion')


                        
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
                        
                    CONFIG_DATA['optional_ticker_bgcolor'] = hex_to_rgb(optional_ticker_bgcolor)
                    CONFIG_DATA['optional_ticker_font_color'] = hex_to_rgb(optional_ticker_font_color)
                    CONFIG_DATA['optional_ticker_speed'] = optional_ticker_speed
                    CONFIG_DATA['optional_ticker_motion'] = optional_ticker_motion       

                except Exception as secondaryscroll:
                    logger.warning('Exception raised during secondaryscroll'+secondaryscroll)
            
        elif tickerSelection == 'media':
            
            tickertype='Media Ticker' 
            tickerTitle=request.POST.get('mediaTickerTitle')
            tickerPriority=request.POST.get('mediaTickerPriority')
            CONFIG_DATA['time_interval']= int(request.POST.get('mediaTickerTimeInterval')) * 60

            static_ticker_condition = request.POST.get('staticTickerEnabler')

            if  static_ticker_condition=='enabled':

                try:  

                    CONFIG_DATA['static_ticker_condition']=True
                    CONFIG_DATA['static_ticker_logo']=True
                    position_static_ticker = request.POST.get('staticPositionBox')
                    CONFIG_DATA['position_static_ticker']=position_static_ticker

                    if position_static_ticker=="center":
                        static_ticker_font_color = request.POST.get('staticFontColor')
                        static_ticker_bgcolor = request.POST.get('staticBgColor')
                        static_ticker_message = request.POST.get('staticTickerMessage')
                        static_ticker_font_type = request.POST.get('staticFontType')
                        static_ticker_font_size = request.POST.get('staticFontSize')
                    elif position_static_ticker=="fullscreen":
                        static_ticker_font_color = '#FFFFFF'
                        static_ticker_bgcolor = '#FFFFFF'
                        static_ticker_message = ""
                        static_ticker_font_type = 'TimesNewRoman'
                        static_ticker_font_size = 'x-large'
                    else:
                        static_ticker_font_color = '#FFFFFF'
                        static_ticker_bgcolor = '#FFFFFF'
                        static_ticker_message = ""
                        static_ticker_font_type = 'TimesNewRoman'
                        static_ticker_font_size = 'x-large'

                        main_ticker_enabler=request.POST.get('StaticScrollingEnable')

                        if main_ticker_enabler=='enabled':

                            main_ticker_message    = request.POST.get('staticScrollingTickerMessage')
                            main_ticker_font    = request.POST.get('staticScrollingFontType')
                            # main_ticker_font_size    = request.POST.get('primaryFontSize')
                            main_ticker_bgcolor    = request.POST.get('staticScrollingBgColor') 
                            main_ticker_font_color    = request.POST.get('staticScrollingFontColor')
                            # main_ticker_speed    = request.POST.get('primaryTickerSpeed')
                            main_ticker_motion    = request.POST.get('staticScrollingTickerMotion')

                            CONFIG_DATA['main_ticker_condition']=True
                            CONFIG_DATA['main_ticker_logo'] = False
                            CONFIG_DATA['main_ticker_font_size'] = "x-large"
                            CONFIG_DATA['main_ticker_bgcolor'] = hex_to_rgb(main_ticker_bgcolor)
                            CONFIG_DATA['main_ticker_font_color'] = hex_to_rgb(main_ticker_font_color)
                            CONFIG_DATA['main_ticker_speed'] = "normal"
                            CONFIG_DATA['main_ticker_motion'] = main_ticker_motion 

                            CONFIG_DATA['main_ticker_message'] = main_ticker_message
                                                        
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
                            
                            if 'top' in position_static_ticker:
                                CONFIG_DATA['main_ticker_position'] = 'down'
                            else:
                                CONFIG_DATA['main_ticker_position'] = 'up'   
                        else:
                            CONFIG_DATA['main_ticker_condition']=False                   
                    
                    CONFIG_DATA['static_ticker_bgcolor'] = hex_to_rgb(static_ticker_bgcolor)
                    CONFIG_DATA['static_ticker_font_color'] = hex_to_rgb(static_ticker_font_color)
                    CONFIG_DATA['static_ticker_message'] = static_ticker_message

                    if static_ticker_font_size == 'x-large':
                        CONFIG_DATA['static_ticker_font_size'] = 120
                        #CONFIG_DATA['static_ticker_image_size'] = 13.45
                    elif static_ticker_font_size == 'large':
                        CONFIG_DATA['static_ticker_font_size'] = 100
                        #CONFIG_DATA['static_ticker_image_size'] = 15.45
                    elif static_ticker_font_size == 'normal':
                        CONFIG_DATA['static_ticker_font_size'] = 80
                        #CONFIG_DATA['static_ticker_image_size'] = 17.45
                    elif static_ticker_font_size == 'small':
                        CONFIG_DATA['static_ticker_font_size'] = 40
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
                                        

                except Exception as staticscroll:
                    logger.warning('Exception raised during staticscroll'+staticscroll)
            else:
                try:
                    # moving_video= request.POST.get('animation_video')
                    moving_ticker_localtion= request.POST.get('dynamicTickerPosition')
                    moving_ticker_center_size=request.POST.get('dynamicTickerLocation')
                    moving_ticker_color=request.POST.get('dynamicTickerBorderColor')

                    CONFIG_DATA['moving_ticker_color']=hex_to_rgb(moving_ticker_color)

                    CONFIG_DATA['moving_ticker_condition']= True
                            
                    CONFIG_DATA['moving_ticker_localtion'] = moving_ticker_localtion
                    CONFIG_DATA['moving_ticker_center_size'] = moving_ticker_center_size
                    
                    if CONFIG_DATA['moving_ticker_localtion'] == "fullscreen":
                        CONFIG_DATA['moving_ticker_localtion'] = "center"
                        CONFIG_DATA['moving_ticker_center_size'] = "full"

                except Exception as animationscroll:
                    logger.warning('Exception raised during animationscroll'+animationscroll)
            
        elif tickerSelection == 'emergency':

            tickertype='Emergency Ticker'
            tickerTitle=request.POST.get('emergencyTickerTitle')
            tickerPriority='Emergency'
            try:
                CONFIG_DATA['emergency_ticker_condition']= True
                CONFIG_DATA['time_interval']= 864000
            except Exception as emergencyscroll:
                logger.warning('Exception raised during emergencyscroll'+emergencyscroll)

        else:
            print('No ticker selected')
        
        CONFIG_DATA['ticker_type']=tickertype
        CONFIG_DATA=json.dumps(CONFIG_DATA, indent=3)

        try:
            data_saver(request,tickertype,CONFIG_DATA,tickerTitle,tickerPriority)
        except Exception as e:
            logger.error("Exception while insertion: "+e)

        try:
            t=TickerDetails.objects.filter(ticker_title=tickerTitle,ticker_priority=tickerPriority,ticker_type=tickertype,ticker_json=CONFIG_DATA,created_on__gte=str(datetime.now()-timedelta(minutes=1))).values()
        except Exception as e:
            logger.error("Exception when fetching for update: "+e)
            t=None
        
        if t!=None:
            
            ticker_id_for_schedule=t.get().get('ticker_id',-1)
            CONFIG_DATA=FileUploader(request,t.get())
            try:
                t.update(ticker_json=CONFIG_DATA)
            except TickerDetails.DoesNotExist  as e:
                logger.error('Unable to update: '+e)
            
            try:
                schedulingticker(request,ticker_id_for_schedule)
            except Exception as e:
                logger.error('Error While schedule: '+e)
        
    except Exception as e:
        logger.error(e)


def data_saver(request,tickertype,CONFIG_DATA1,tickerTitle,tickerPriority):
    
    tickerobj=TickerDetails()

    tickerobj.ticker_type=tickertype

    tickerobj.ticker_title=tickerTitle

    tickerobj.ticker_json=CONFIG_DATA1
    
    if request.POST.get('tickerSelecter')== 'emergency' or request.POST.get('scrollingTickerPriority') == 'Emergency':
        tickerobj.ticker_start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tickerobj.frequency = str(1)
        tickerobj.occuring_days = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tickerobj.ticker_end_time=(datetime.now()+timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
    
    elif request.POST.get('scheduleEnabler') == 'enabled':
        tickerobj.ticker_start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tickerobj.frequency = str(1)
        tickerobj.occuring_days = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tickerobj.ticker_end_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    else:
        if request.POST.get('recurring')=='enabled':
            
            tickerobj.ticker_start_time=dateformatter(request.POST.get('startDate'),'time')
            tickerobj.ticker_end_time=dateformatter(request.POST.get('endDate'),'time')

            tickerobj.frequency = request.POST.get('delay')

            occuring_days=str()

            if request.POST.get('Sunday')=="enabled":
                occuring_days+='Sunday,'

            if request.POST.get('Monday')=="enabled":
                occuring_days+='Monday,'

            if request.POST.get('Tuesday')=="enabled":
                occuring_days+='Tuesday,'

            if request.POST.get('Wednesday')=="enabled":
                occuring_days+='Wednesday,'

            if request.POST.get('Thursday')=="enabled":
                occuring_days+='Thursday,'

            if request.POST.get('Friday')=="enabled":
                occuring_days+='Friday,'

            if request.POST.get('Saturday')=="enabled":
                occuring_days+='Saturday'
            
            tickerobj.occuring_days = occuring_days

        else:
            tickerobj.ticker_start_time=dateformatter(request.POST.get('startDate'),'time')
            tickerobj.frequency = str(1)
            tickerobj.occuring_days = dateformatter(request.POST.get('startDate'),'days')
            tickerobj.ticker_end_time=dateformatter(request.POST.get('startDate'),'time')

    # print(tickerobj.ticker_start_time,tickerobj.ticker_end_time)
    tickerobj.wings=str(request.POST.getlist('wingSelection'))
    tickerobj.floors=str(request.POST.getlist('floorSelection'))
    tickerobj.rooms=str(request.POST.getlist('roomSelection'))
    tickerobj.roomTypeSelection=str(request.POST.getlist('roomTypeSelection'))

    tickerobj.ticker_priority=tickerPriority

    tickerobj.created_by=request.user.username
    tickerobj.created_on=datetime.now()
    
    tickerobj.modified_by=request.user.username
    tickerobj.modified_on=datetime.now()
    
    tickerobj.is_active=1
    tickerobj.is_deleted=0

    tickerobj.save()

def filterData(file):

    roomType = {'All'}
    floor = {'All'}
    key = ['All']

    document = xml.etree.ElementTree.parse(file).getroot()

    for item in document.findall('node'):
        if item.get('room_type') != None:
            roomType.add(item.get('room_type'))

    a=sorted(roomType)

    roomTypeValue = 'All'#input('Choice Room Type : ')
    for item in document.findall('node'):
        if (roomTypeValue == 'All' or item.get('room_type') == roomTypeValue) and item.get('room_type') != None:
            floor.add(item.get('floor'))
    b=sorted(floor)

    floorValue = 'All'#input('Choice Floor : ')
    for item in document.findall('node'):
        if (floorValue == 'All' or item.get('floor') == floorValue) and item.get('floor') != None:
            key.append(item.get('key_no'))
    c=sorted(key)

    wings=list()
    wings.append('All')

    return {'wings':wings,'roomtype':a,'floor':b,'keys':c}