import json
from datetime import datetime,timedelta
import xml.etree.ElementTree as ET
from .models import SetUp
from ticker_management.tasks import callticker
from .models import TickerDetails
from pathlib import Path
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from ticker_dashboard.settings import BASE_DIR,AUTH_TOKEn_API

import logging
logger=logging.getLogger('dashboardLogs')

def replacer(s):
    return str(s).replace('{','').replace('}','').replace(' ','')

def addrecurringtime(start_time,end_time,frequency):
   minutes=set()
   hours=set()
   day=set()
   month=set()

   while (start_time<end_time):
       minutes.add(int(start_time.strftime('%M')))
       hours.add(int(start_time.strftime('%H')))
       day.add(int(start_time.strftime('%d')))
    #    day_of_week.add(start_time.strftime('%A'))
       month.add(int(start_time.strftime('%m')))

       start_time+=timedelta(minutes=frequency)

   return {"hours":replacer(hours),"minutes":replacer(minutes),
           "days":replacer(day)#"day_of_week":replacer(day_of_week)
           ,"month":replacer(month)}

def xmlFileRead(tagList,idList,root):
    
    for id in idList:

        for child in root:
            if child.get('key_id') and child.get('key_id') == str(id):
                tagList.append(child.get('name'))
    st=str()
    for i in tagList:
        st+=str(i)+' '

    return st.strip()

def roomConfigurations(request):
    logger.info('Inside roomConfiguration function')

    wings=request.POST.getlist('wingSelection')
    floors=request.POST.getlist('floorSelection')
    rooms=request.POST.getlist('roomSelection')

    print(wings,type(wings))
    print(floors,type(floors))
    print(rooms,type(rooms))

    idList = list()

    file=open(f"{str(BASE_DIR)}/static/resources/resource.json")

    datafromdvs=json.load(file)


    tree = ET.parse(f"{str(BASE_DIR)}/static/resources/resource.xml")
    root = tree.getroot()

    tagList=list()

    if (len(rooms)==1 and rooms[0]=='All'):
        if (len(floors)==1 and floors[0]=='All'):
            if (len(wings)==1 and wings[0]=='All'):
                
                return '.*'

            else:

                for parWing in wings:

                    for items in datafromdvs.get('data'):

                        if items.get('wing_name')!=None and items.get('wing_name') == parWing:
                            
                            idList.append(items.get('id'))
                
                """
                
                We are fetching data from dvs.json and resource.xml because resource.xml not contains wings info but dvs contains all info.
                But it also have some problems like dvs.json contains key_name as Single-0000 but resource.xml contains it as Standard-0000.
                This is the reason for 2 file system.

                """

                return xmlFileRead(tagList,idList,root)           
        
        else:

            
            for parFloor in floors:

                for items in datafromdvs.get('data'):

                    if items.get('floor_name')!=None and items.get('floor_name') == parFloor:
                        
                        idList.append(items.get('id'))
            
           
            return xmlFileRead(tagList,idList,root)

    else:
            
        for parRoom in rooms:

            for items in datafromdvs.get('data'):

                if items.get('key_number')!=None and items.get('key_number') == parRoom:
                    
                    idList.append(items.get('id'))
        
        print("inside 2")
        return xmlFileRead(tagList,idList,root)

def schedule_tasks(ticker_id,command):

    logger.info('Inside schedule_tasks function')

    ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()

    # print(ticker_id,ticker_obj.get())
    
    start_dateobj=datetime.strftime(ticker_obj.get().get('ticker_start_time'), '%Y-%m-%d %H:%M:%S')
    end_dateobj=datetime.strftime(ticker_obj.get().get('ticker_end_time'), '%Y-%m-%d %H:%M:%S')

    start_dateobj=datetime.strptime(start_dateobj,'%Y-%m-%d %H:%M:%S')
    end_dateobj=datetime.strptime(end_dateobj,'%Y-%m-%d %H:%M:%S')

    print(start_dateobj,end_dateobj)
    
    if (start_dateobj==end_dateobj):
        # print("4")

        year = start_dateobj.strftime("%Y")
        # print("4",year,type(year))

        month = start_dateobj.strftime("%m")

        day = start_dateobj.strftime("%d")

        hour = start_dateobj.strftime("%H")

        minute = int(start_dateobj.strftime("%M"))

        schedule,created=CrontabSchedule.objects.get_or_create(month_of_year=month,day_of_month=day,hour=hour,minute=minute)
        task=PeriodicTask.objects.create(crontab=schedule,task='ticker_management.tasks.callticker',name='ScheduledTicker '+str(ticker_id),args=json.dumps((command,ticker_id)))

    else:
        
        frequency=str(ticker_obj.get()['frequency'])

        if 'minutes' in frequency:
            frequency=frequency.split(" ")[0]
        else:
            frequency=frequency.split(" ")[0]
            frequency=int(frequency)*60
        
        data=addrecurringtime(start_dateobj,end_dateobj,int(frequency))

        if ',' in data['days']:

            week=str(ticker_obj.get()['occuring_days']).split(',')

            all_week= ['Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday']

            for i in range(len(week)):
                if i==0:
                    week_number=str(all_week.index(week[i]))+','
                elif i==len(week)-1:
                    week_number+=str(all_week.index(week[i]))
                else:
                    week_number+=str(all_week.index(week[i]))+','
        
        else:
            week_number=str(start_dateobj.strftime('%A'))

        print(data,week_number)

        schedule,created=CrontabSchedule.objects.get_or_create(month_of_year=data.get('month'),day_of_month=data['days'],hour=data['hours'],minute=data['minutes'],day_of_week=week_number)
        task=PeriodicTask.objects.create(crontab=schedule,task='ticker_management.tasks.callticker',name='ScheduledTicker '+str(ticker_id),args=json.dumps((command,ticker_id)))

def schedulingticker(request,ticker_id):
    logger.info('Inside scheduleticker function')

    setup=SetUp.objects.filter(id=1).values()

    FQDN=setup.get()['FQDN']
    Dvs_Token=setup.get()['Dvs_Token']
    Rundeck_Token=setup.get()['Rundeck_Token']
    Rundeck_Api_Version=setup.get()['Rundeck_Api_Version']
    Ticker_FQDN=setup.get()['Ticker_FQDN']
    Rundeck_Start_Job=setup.get()['Rundeck_Start_Job']

    configuration=roomConfigurations(request)
    
    try:
        auth=AUTH_TOKEn_API
    except:
        auth="YWRtaW46YWRtaW4xMjM0"

    json_data = {
        'argString': f'-whichnode {configuration} -FQDN {Ticker_FQDN} -jsonFile {ticker_id} -BasicAuth {auth}',
    }

    print(auth)
    
    if (len(json_data)>0):
        if request.POST.get('tickerSelecter')== 'emergency' or request.POST.get('scheduleEnabler') == 'enabled':
            callticker(json_data,ticker_id)
        else:
            schedule_tasks(ticker_id,json_data)
    else:
        print("No scheduled processes")
