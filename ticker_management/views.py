import os
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json
import subprocess
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
    roomTypeData = set()
    wingData = set()
    floorData = set()
    keyData = set()
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
    data['scheduleData']=filterData()
    if request.method == 'POST':


        # print(request.POST.get('startDate'),request.POST.get('endDate'))

        # print(request.POST.get('Sunday'),request.POST.get('Monday'))
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
    eventData = dict()
    events = list()
    ticker_obj=TickerDetails.objects.values('ticker_id','ticker_title','ticker_start_time','ticker_end_time')
    for item in ticker_obj:
        data = dict()
        data['groupId']=item.get('ticker_id')
        data['title']=item.get('ticker_title')
        data['start']=item.get('ticker_start_time').strftime('%Y-%m-%dT%H:%M:%S')
        data['end']=item.get('ticker_end_time').strftime('%Y-%m-%dT%H:%M:%S')
        events.append(data)
    eventData['events'] = events
    event = json.dumps(eventData)
    # txt = str(event)
    # txt = txt.replace("{'","{").replace("':",":").replace(", '",", ")
    with open('{0}/../static/resources/events.json'.format(BASE_DIR), 'w') as f:
        f.write(str(event))
    return render(request, 'scheduled.html',{'user':request.user.username})

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
    # print(dvs_data.get())
    FQDN=dvs_data.get().get('FQDN')
    Dvs_Token=dvs_data.get().get('Dvs_Token')
    dvs_data="curl -s --location --request POST 'https://{2}/dvs/api/key/selectR' --header 'Content-Type: application/vnd.digivalet.v1+json' --header 'Access-Token: {3}' --data-raw '{0}' | jq  > {1}/../static/resources/resource.json".format('{}',BASE_DIR,FQDN,Dvs_Token)
    os.system(dvs_data)

@api_view(['GET', 'POST', 'DELETE'])
def taskPost(request,pk="0"):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        d={}
        d['ip']=ip
        d.update(request.POST)
        for i,j in d.items():
            if type(j) == list:
                d[i] = j[0]
        query_dict = QueryDict('', mutable=True)
        query_dict.update(d)
        serializer = TaskSerializer(data=query_dict)
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


def details(request, id):
    data = dict()
    dvs_data=SetUp.objects.filter(id=1).values()
    FQDN=dvs_data.get().get('FQDN')
    Dvs_Token=dvs_data.get().get('Dvs_Token')
    Rundeck_Token=dvs_data.get().get('Rundeck_Token')
    # rundeck_out="curl --location --request GET 'https://{0}/r/api/17/execution/6036/output' --header 'X-Rundeck-Auth-Token: {1}'".format(FQDN,Rundeck_Token)
    r = requests.get(f"https://{FQDN}/r/api/17/execution/6036/output", headers={"X-Rundeck-Auth-Token":Rundeck_Token})
    try:
        # process = subprocess.Popen(rundeck_out, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output = process.stderr.read()
        # exitstatus = process.wait()
        exitstatus = 0
        if exitstatus == 0:
            xmlDocument = xml.etree.ElementTree.parse(process.stdout).getroot()
            xmlDocument = xml.etree.ElementTree.parse(process.stdout).getroot()
            tree = ET.parse(r.text).getroot()
            for item in xmlDocument.iter('entry'):
                if item.get('level') == 'ERROR':
                    data['log'] = item.get('log')
                    data['room'] = item.get('node')
                    print(data)
            return render(request, 'tickerdetails.html')
        else:
            return HttpResponse(output.decode('utf-8'))
    except Exception as e:
        return HttpResponse(e)
    # try:
    #     r = requests.get(f"https://{FQDN}/r/api/17/execution/6036/output", headers={"X-Rundeck-Auth-Token":Rundeck_Token})
    #     tree = ET.parse(r.text)
    #     root = tree.getroot()
    #     xmlDocument = root
    #     items = xmlDocument.getElementsByTagName('entry')
    #     print(items[1].attributes['time'].value)
    #     print(xmlDocument.tag)
    #     print(xmlDocument.attrib)
    #     for neighbor in xmlDocument.iter('entry'):
    #         print(neighbor.attrib)
    #     # for item in xmlDocument.findall('entries'):
    #     #     print(item.get('entry').attrib)

    #     return HttpResponse("hello")

    # # for entries_xml in root.findall('entries'):
    # #     entry_data = entries_xml.find('entry').text
    # #     # name = country.get('name')
    # #     print(entry_data)
    # # print(root)
    #     return HttpResponse("Data Saved!")
    # except OSError as exc:
    #     if exc.errno == 36:
    #         return HttpResponse(r.text)