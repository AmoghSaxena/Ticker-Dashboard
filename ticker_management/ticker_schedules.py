import json
from datetime import datetime,timedelta
from .models import SetUp
from ticker_management.tasks import callticker
from .models import TickerDetails
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from ticker_dashboard.settings import AUTH_TOKEN_API
from threading import Thread

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

def schedule_tasks(basicTickerInfo,ticker_obj):
    try:
        logger.info('Inside schedule_tasks function')
        start_dateobj=datetime.strftime(ticker_obj.get().get('ticker_start_time'), '%Y-%m-%d %H:%M:%S')
        end_dateobj=datetime.strftime(ticker_obj.get().get('ticker_end_time'), '%Y-%m-%d %H:%M:%S')

        start_dateobj=datetime.strptime(start_dateobj,'%Y-%m-%d %H:%M:%S')
        end_dateobj=datetime.strptime(end_dateobj,'%Y-%m-%d %H:%M:%S')

        print(start_dateobj,end_dateobj)

        ticker_id=ticker_obj.get()['ticker_id']
        
        if (start_dateobj==end_dateobj):

            year = start_dateobj.strftime("%Y")

            month = start_dateobj.strftime("%m")

            day = start_dateobj.strftime("%d")

            hour = start_dateobj.strftime("%H")

            minute = int(start_dateobj.strftime("%M"))

            schedule,created=CrontabSchedule.objects.get_or_create(month_of_year=month,day_of_month=day,hour=hour,minute=minute)
            task=PeriodicTask.objects.create(crontab=schedule,task='ticker_management.tasks.callscheduledticker',name='ScheduledTicker '+str(ticker_id),args=json.dumps((basicTickerInfo,ticker_id)))

            return {"message":"Success"}
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
            print('GOAL')
            task=PeriodicTask.objects.create(crontab=schedule,task='ticker_management.tasks.callscheduledticker',name='ScheduledTicker '+str(ticker_id),args=json.dumps((basicTickerInfo,ticker_id)))
            return {"message":"Success"}
    except Exception as err:
        logger.error(err)
        return {"message":"Error while periodic schedules: "+str(err)}

def schedulingticker(request,ticker_id):
    try:
        logger.info('Inside scheduleticker function')
        
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()

        setup=SetUp.objects.filter(id=1).values()

        FQDN=setup.get()['FQDN']
        Dvs_Token=setup.get()['Dvs_Token']
        Rundeck_Token=setup.get()['Rundeck_Token']
        Rundeck_Api_Version=setup.get()['Rundeck_Api_Version']
        Ticker_FQDN=setup.get()['Ticker_FQDN']
        Rundeck_Start_Job=setup.get()['Rundeck_Start_Job']

        wings_str=ticker_obj.get()['wings']
        floors_str=ticker_obj.get()['floors']
        rooms_str=ticker_obj.get()['rooms']

        if wings_str=='All' and floors_str=='All' and rooms_str=='All':
            configuration=".*"
        else:
            configuration=str(rooms_str).strip("[]").replace("'",'').replace(",","")

        print(configuration)
        
        try:
            auth=AUTH_TOKEN_API
        except:
            auth="YWRtaW46YWRtaW4xMjM0"
        
        # print('GOAL')
        # print(ticker_obj.get()['ticker_json'],json.loads(ticker_obj.get()['ticker_json']))

        basicTickerInfo={
            'FQDN':FQDN,
            'Dvs_Token':Dvs_Token,
            'Rundeck_Token':Rundeck_Token,
            'Rundeck_Api_Version':Rundeck_Api_Version,
            'Ticker_FQDN':Ticker_FQDN,
            'Rundeck_Start_Job':Rundeck_Start_Job,
            'time_interval':int(json.loads(ticker_obj.get()['ticker_json'])['time_interval'])
        }

        json_data = {
            'argString': f'-whichnode "{configuration}" -FQDN {Ticker_FQDN} -jsonFile {ticker_id} -BasicAuth {auth}',
        }

        basicTickerInfo['json_data']=json_data

    except Exception as err:
        logger.error(err)
        return {"message":"Error while schedules: "+str(err)}
    
    data=dict()

    if (len(json_data)>0):
        if request.POST.get('tickerSelecter')== 'emergency' or request.POST.get('scheduleEnabler') == 'enabled' or request.POST.get('scrollingTickerPriority')=='Emergency':
            Thread(target=callticker,args=(basicTickerInfo,ticker_obj)).start()
        else:
            data=schedule_tasks(basicTickerInfo,ticker_obj)
        
        if data.get('message','0')=='0':
            return {"message":'Success'}
        else:
            return data
    else:
        logger.info("No scheduled processes")
