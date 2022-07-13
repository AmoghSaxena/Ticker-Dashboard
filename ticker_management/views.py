import os
import json
import xml.etree.ElementTree
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from ticker_management.gadget import datagetter,filterData
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from datetime import datetime
from ticker_management.models import TickerDetails,TickerHistory,SetUp
from ticker_management.tasks import test_fun
from pathlib import Path
from .forms import LoginForm
from rest_framework.decorators import api_view
from django.http import QueryDict
from .serializers import TaskSerializer, TaskSerializerConfig
from rest_framework.response import Response
from .models import Task
#Api
BASE_DIR = Path(__file__).resolve().parent
def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                user_login(request, user)
                return redirect(request.GET['next'])
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})

@login_required
def index(request):
    active_ticker_length=TickerDetails.objects.all().filter(is_active=1)
    active_ticker=TickerDetails.objects.all().filter(is_active=1).order_by('modified_on').reverse()[:5]
    total_ticker=TickerHistory.objects.all()
    history_count = 8
    ticker_count={
        'active':len(active_ticker_length),
        'history':history_count,
        'total':(history_count+len(active_ticker_length)),
        'events': 12,
        'active_ticker_data':active_ticker,
        'user':request.user.username
    }
    return render(request, 'index.html',ticker_count)

def filterData():
    DVSDATA = dict()
    roomTypeData = {'All'}
    wingData = {'All'}
    floorData = {'All'}
    keyData = {'All'}
    xmlDocument = xml.etree.ElementTree.parse(f"{BASE_DIR}/resources/res.xml").getroot()
    jsonDocument = json.load(open(f"{BASE_DIR}/resources/resource.json"))

    for item in xmlDocument.findall('node'):
        if item.get('room_type') != None:
            roomTypeData.add(item.get('room_type'))
        if item.get('floor') != None:
            floorData.add(item.get('floor'))
        if item.get('key_no') != None:
            keyData.add(item.get('key_no'))

    for item in jsonDocument.get('data'):
        wingData.add(item.get('wing_name'))
    
    DVSDATA["roomType"]=sorted(roomTypeData)
    DVSDATA["wing"] = sorted(wingData)
    DVSDATA["floor"] = sorted(floorData)
    DVSDATA["key"] = sorted(keyData)
    
    return DVSDATA


@login_required
def createTicker(request):
    syncDVSData()
    
    data = {
            'pos_box':[
                'top-right',
                'top-left',
                'bottom-right',
                'bottom-left',
                'center',
                'fullscreen'
                ],
            
            'font_style':[
                'TimesNewRoman',
                'MyriadProFont',
                'Ubuntu',
                'Russian',
                'Chinese',
                'Japanese',
                'Arabic',
                'Turkish',
                'Spanish',
                'French',
                'Hindi'
                ],

            'font_size':[
                'x-large',
                'large',
                'normal',
                'small'
                ],

            'position':[
                'up',
                'down'
                ],

            'logo_position':[
                'left',
                'right'
                ],

            'speed':[
                'fast',
                'normal',
                'slow',
                'very-slow'
                ],
            
            'motion':[
                'left-right',
                'right-left'
                ],

            'location':[
                'small',
                'normal',
                'large'
                ],
                
            'emergency_ticker_list':[
                'Earthquake',
                'Fire',
                'Active Shooting',
                'General Evacuation',
                'Custom'
                ],

            'priority':[
                'High',
                'Medium',
                'Low'
            ],
            'user':request.user.username,
            'frequency' :[
                '15 minutes', 
                '30 minutes', 
                '45 minutes', 
                '1 hour', 
                '75 minutes', 
                '90 minutes', 
                '105 minutes', 
                '2 hour', 
                '3 hour',
                '4 hour',  
                '5 hour',  
                '6 hour',  
                '7 hour',  
                '8 hour',
                '12 hour',
                '24 hour'  
            ],
            'days' :['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        }
    
    data['scheduledata']=filterData()


    if request.method == 'POST':
        # print(request.POST.get('tickerSelecter'))
        datagetter(request)
        
        return redirect(index)
        # if (
        #     request.POST.get('static_ticker_enabler')=='' or 
        #     request.POST.get('primary_ticker_enabler')=='' or 
        #     request.POST.get('secondary_ticker_enabler')=='' or 
        #     request.POST.get('animation_ticker_enabler')=='' or 
        #     request.POST.get('emergency_ticker_enabler')==''
        #    ):
        #     # datagetter(request)
        #     # return redirect(preview,id=datagetter(request).get('ticker_id'))
        # else:
        #     return render(request, 'createticker.html', data)
    else:
        return render(request, 'createticker.html', data)


@login_required
def updateTicker(request,ticker_id):
    pass


@login_required
def active(request):
    data=TickerDetails.objects.all().filter(is_active=1).values()
    tickerDataList=list()
    for item in data:
        tickerDataList.append(item)
    tickerDataList=sorted(tickerDataList,key=lambda item: item['ticker_id'],reverse=True)
    tmp={'tickerDataList':tickerDataList,'user':request.user.username}
    return render(request, 'active.html',tmp)

@login_required
def history(request):
    data=TickerDetails.objects.all().filter(is_active=1).values()
    tickerDataList=list()
    for item in data:
        tickerDataList.append(item)
    tickerDataList=sorted(tickerDataList,key=lambda item: item['ticker_id'],reverse=True)
    tmp={'tickerDataList':tickerDataList,'user':request.user.username}
    return render(request, 'history.html',tmp) 
        
@login_required
def scheduled(request):
    events= [
        {
            'title': 'Emergency',
            'start': '2022-08-07'
        },
        {
            'title': 'Dynamic',
            'start': '2022-07-07',
            'end': '2022-07-10'
        },
        {
            'groupId': 999,
            'title': 'Primary',
            'start': '2022-07-09T16:00:00'
        },
        {
            'groupId': 999,
            'title': 'Dynamic',
            'start': '2022-07-16T16:00:00'
        },
        {
            'title': 'Secondary',
            'start': '2022-07-11',
            'end': '2022-07-13'
        },
        {
            'title': 'Emergency',
            'start': '2022-07-12T10:30:00',
            'end': '2022-07-12T12:30:00'
        },
        {
            'title': 'Static',
            'start': '2022-07-12T12:00:00'
        },
        {
            'title': 'Primary',
            'start': '2022-07-12T14:30:00'
        },
        {
            'title': 'Primary',
            'start': '2022-07-12T17:30:00'
        },
        {
            'title': 'media',
            'start': '2022-07-12T20:00:00'
        },
        {
            'title': 'Emergency',
            'start': '2022-07-13T07:00:00'
        }
    ]
    
    return render(request, 'scheduled.html',{'user':request.user.username, 'events':events})

def isEdit(request):
    pass

def isRestore(request):
    pass

def isDelete(request, id):
    tickerDataDelete = TickerDetails.objects.get(ticker_id=id)  
    tickerDataDelete.delete()  
    return redirect(active)

def syncDVSData():
    dvs_data=SetUp.objects.filter(id=1).values()
    print(dvs_data.get())
    FQDN=dvs_data.get().get('FQDN')
    Dvs_Token=dvs_data.get().get('Dvs_Token')
    dvs_data="curl -s --location --request POST 'https://{2}/dvs/api/key/selectR' --header 'Content-Type: application/vnd.digivalet.v1+json' --header 'Access-Token: {3}' --data-raw '{0}' | jq  > {1}/../static/resources/resource.json".format('{}',BASE_DIR,FQDN,Dvs_Token)
    os.system(dvs_data)

@api_view(['GET', 'POST', 'DELETE'])
def taskPost(request,pk="0"):
    if request.method == 'POST':
        # print(request)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        d={}
        d['ip']=ip
        d.update(request.POST)
        print(d)
        for i,j in d.items():
            if type(j) == list:
                d[i] = j[0]
        query_dict = QueryDict('', mutable=True)
        query_dict.update(d)
        serializer = TaskSerializer(data=query_dict)
        print(str(serializer))
        print("........................................")
        print("serializer isValid: " + str(serializer.is_valid()))
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'GET':
        tasks = Task.objects.all().order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        print(serializer)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        serializer = TaskSerializer(data=request.data)
        p=serializer.initial_data
        q=int(p.get('id'))
        print(type(q))
        task = Task.objects.get(id=q)
        task.delete()

        return Response('Item succsesfully delete!')


@api_view(['GET'])
def configApi(request,pk="0"):
    if request.method == 'GET':
        serializer = TaskSerializerConfig(data=request.data)
        p=serializer.initial_data
        q=int(p.get('ticker_id'))
        tasks = TickerDetails.objects.filter(ticker_id=q).values_list('ticker_json')
        serializer = TaskSerializerConfig(tasks.get(), many=False)
        return Response(json.loads(serializer._args[0][0]))






def pending(request):
    return render(request, 'pending.html',{'user':request.user.username}) 

def schedule(request):
        # if request.method == 'POST':
        
    #     a=request.POST.get('wingselection')
    #     b=request.POST.get('floorselection')
    #     c=request.POST.get('roomselection')

    #     if (request.POST.get('scheduleenabler')!=None):
    #         print('Inside enabler')
    #     else:
    #         print('Outside enabler')
        
    #     start_date=request.POST.get('start_date')
    #     end_date=request.POST.get('end_date')

    #     created_for=str(a)+' '+str(b)+' '+str(c)
        
    #     t=TickerDetails.objects.filter(ticker_id=int(id)).values()

    #     t.update(ticker_start_time=start_date,ticker_end_time=end_date,created_for=created_for)

    #     return redirect('/')

    # else:
    #     roomconfig=filterData('resources/resourcexml')
    #     roomconfig['ticker_id']=id
    #     frequency = [
    #         '15 minutes', 
    #         '30 minutes', 
    #         '45 minutes', 
    #         '1 hour', 
    #         '75 minutes', 
    #         '90 minutes', 
    #         '105 minutes', 
    #         '2 hour', 
    #         '3 hour',
    #         '4 hour',  
    #         '5 hour',  
    #         '6 hour',  
    #         '7 hour',  
    #         '8 hour',
    #         '12 hour',
    #         '24 hour'  
    #         ]

    #     days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

    #     roomconfig['routine']=frequency
    #     roomconfig['routine_days']=days

    # now = datetime.now() # current date and time

    # year = now.strftime("%Y")

    # month = now.strftime("%m")

    # day = now.strftime("%d")

    # hour = int(now.strftime("%H"))

    # minute = int(now.strftime("%M"))+2

    # if minute>=60:
    #     hour+=minute%60
    #     minute=minute/60

    # schedule,created=CrontabSchedule.objects.get_or_create(month_of_year=month,day_of_month=day,hour=hour,minute=minute)
    # task=PeriodicTask.objects.create(crontab=schedule,task='ticker_management.tasks.test_fun',name='trying_to_make_same'+str(5))
    # return HttpResponse('day:{},month:{},{}:{}'.format(day,month,hour,minute))

    # print(request.POST.get('delay'))
    pass

def preview(request,id):
    if request.method == 'POST':
        # print(request.POST.get('ticker_id_field'))
        id=request.POST.get('ticker_id_field')

        # print(roomconfig.get('ticker_id','no data found'))

        return redirect(schedule,id=id)

        # return render(request, 'schedule.html',roomconfig)
    else:
        t=TickerDetails.objects.filter(ticker_id=int(id)).values()
        return render(request, 'preview.html',t.get())

