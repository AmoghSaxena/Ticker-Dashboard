import os
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json
import subprocess
import xml.etree.ElementTree
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as user_login
from django.contrib import messages
from ticker_management.gadget import datagetter,filterData
from django.http import HttpResponse
# from django_celery_beat.models import PeriodicTask,CrontabSchedule
from datetime import date
from ticker_management.models import TickerDetails,TickerHistory,SetUp,RundeckLog
from pathlib import Path
from .forms import LoginForm, ChangePassword
from rest_framework.decorators import api_view
from django.http import QueryDict
from .serializers import TaskSerializer, TaskSerializerConfig
from rest_framework.response import Response
from .models import Task
from ticker_management.rundecklog import initial_data
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
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
    active_ticker_length=TickerDetails.objects.all().filter()
    active_ticker=TickerDetails.objects.all().filter().order_by('modified_on').reverse()[:5]
    total_ticker=TickerHistory.objects.all()
    today_event=TickerDetails.objects.filter(ticker_start_time__lte=str(date.today())+str(" 23:59:59"),ticker_start_time__gt=str(date.today())+str(" 00:00:00"))
    history_count = 8
    ticker_count={
        'active':len(active_ticker_length),
        'history':history_count,
        'total':(history_count+len(active_ticker_length)),
        'events': len(today_event),
        'active_ticker_data':active_ticker,
        'user':request.user.username
    }
    return render(request, 'index.html',ticker_count)


@login_required
def createTicker(request):
    syncDVSData(request)
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
                'normal',
                'fast',
                'slow',
                'very-slow'
                ],
            
            'motion':[
                'right-left',
                'left-right'
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
                '5 minutes',
                '10 minutes',
                '15 minutes', 
                '30 minutes', 
                '45 minutes', 
                '1 hour',
                '75 minutes',
                '90 minutes'
                '105 minutes'
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
    data['scheduleData']=filterData(request)
    if request.method == 'POST':
        datagetter(request)
        return redirect(index)
    else:
        return render(request, 'createticker.html', data)


@login_required
def updateTicker(request,ticker_id):
    pass


@login_required
def active(request):
    data=TickerDetails.objects.all().filter().values()
    tickerDataList=sorted(data,key=lambda item: item['ticker_id'],reverse=True)
    data={'tickerDataList':tickerDataList,'user':request.user.username}
    return render(request, 'active.html',data)

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
    event = json.dumps(eventData,indent = 3)
    with open('{0}/../static/resources/events.json'.format(BASE_DIR), 'w') as f:
        f.write(str(event))
    return render(request, 'scheduled.html',{'user':request.user.username})

@login_required
def history(request):
    data=TickerDetails.objects.all().filter(is_active=1).values()
    tickerDataList=list()
    for item in data:
        tickerDataList.append(item)
    tickerDataList=sorted(tickerDataList,key=lambda item: item['ticker_id'],reverse=True)
    data={'tickerDataList':tickerDataList,'user':request.user.username}
    return render(request, 'history.html',data) 
        


@login_required
def detail(request, id):
    try:
        ticker_obj=TickerDetails.objects.filter(ticker_id=int(id)).values()
        logObject = list()
        if ticker_obj.get().get('rundeckid')!=None:
            logObject.append(initial_data(ticker_obj))
            rundeckLogData=RundeckLog.objects.all().filter(ticker_id=int(id)).values()
            rundeckLog=sorted(rundeckLogData,key=lambda item: item['rundeck_id'],reverse=True)
        else:
            rundeckLog=list()
            dictwithoutrundeckid={'rundeck_id': "None", 'ticker_id': ticker_obj.get().get('ticker_id'), 'ticker_title': ticker_obj.get().get('ticker_title'), 'execution': "pending", 'successfull_nodes':
             "None", 'failed_nodes': 'None', 'tv_status': 'None', 'iPad_status': 'None'}
            rundeckLog.append(dictwithoutrundeckid)
        return render(request, 'tickerdetail.html' ,{'rundeckLog':rundeckLog, 'logObject':logObject})
    except Exception as e:
        return HttpResponse('Error: '+str(e))

@login_required
def isEdit(request):
    pass

@login_required
def isRestore(request):
    pass

@login_required
def isDelete(request, id):
    try:
        tickerDataDelete = TickerDetails.objects.get(ticker_id=id)
        if tickerDataDelete.get('main_ticker_condition','not found')==True and tickerDataDelete.get('main_ticker_logo','not found')==True:
            image_name=tickerDataDelete.get('main_ticker_logo_name')
        elif tickerDataDelete.get('static_ticker_condition','not found')==True and tickerDataDelete.get('static_ticker_logo','not found')==True:
            image_name=tickerDataDelete.get('static_ticker_logo_name')
        elif tickerDataDelete.get('moving_ticker_condition','not found')==True:
            image_name=tickerDataDelete.get('moving_ticker_logo_name')
        elif  tickerDataDelete.get('emergency_ticker_condition','not found')==True:
            image_name=tickerDataDelete.get('emergency_ticker_logo_name')
    except Exception as e:
        messages.info(request, 'Specificied ID not found')
        return redirect(active)
    try:
        os.remove(image_name.split('/')[-1])
    except Exception as e:
        print("No image found!",e)
    try:
        tickerDataDelete.delete()  
        return redirect(active)
    except Exception as e:
        messages.info(request, 'Unable to delete specificied ID')
        return redirect(active)

@login_required
def changePassword(request):
    # setupMail()
    form = ChangePassword(request.POST or None)
    msg = None
    try:
        if request.method == 'POST':
            old = request.POST.get('oldPassword')
            new = request.POST.get('newPassword')
            if check_password(old, request.user.password):
                if form.is_valid():
                    request.user.set_password(new)
                    newuser = request.user.save()
                    update_session_auth_hash(request, newuser)
                    msg = 'Your password was successfully updated!'
                else:
                    msg = 'Error validating the form'
            else:
                msg = 'Invalid credentials'
        return render(request, 'changepassword.html', {'form': form, 'msg': msg})
    except Exception as e:
        return HttpResponse(e)


@login_required
def syncDVSData(request):
    dvs_data=SetUp.objects.filter(id=1).values()
    # print(dvs_data.get())
    FQDN=dvs_data.get().get('FQDN')
    Dvs_Token=dvs_data.get().get('Dvs_Token')
    dvs_data="curl -s --location --request POST 'https://{2}/dvs/api/key/selectR' --header 'Content-Type: application/vnd.digivalet.v1+json' --header 'Access-Token: {3}' --data-raw '{0}' | jq  > {1}/../static/resources/resource.json".format('{}',BASE_DIR,FQDN,Dvs_Token)
    os.system(dvs_data)

@login_required
def filterData(request):
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

def setupMail():
    try:
        subject = "Hello"
        body = ""
        emailQueue = ['temper.projectgroup@gmail.com']
        email = EmailMessage(subject, body, to=emailQueue)
        email.send()
    except Exception as e:
        print(e)
