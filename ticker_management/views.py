import os, re
import requests
import json
import xml.etree.ElementTree as XMLReader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as user_login
from django.contrib import messages
from ticker_management.gadget import dataSetter
from datetime import date,datetime,timedelta
from ticker_management.models import TickerDetails,TickerHistory,SetUp,RundeckLog
from ticker_management.node import checkPriority
from .forms import LoginForm, ChangePassword
from django.http import QueryDict
from .serializers import TaskSerializer, TaskSerializerConfig
from ticker_management.node import getTickerId,removeDuplicate
from ticker_management.tasks import callscheduledticker
from threading import Thread
from ticker_management.gadget import dateformatter
#### Error Code ####
from .APIStatus import *

#### Rest Framework ####
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from ticker_management.rundecklog import rundeck_update, abortTicker, killTicker
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db.models import Q
from ticker_dashboard.settings import BASE_DIR,AUTH_TOKEN_API

# #Api
# BASE_DIR = Path(__file__).resolve().parent
def base(request):
    return redirect('/ticker')

#Loggers
import logging
logger=logging.getLogger('dashboardLogs')

def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                user_login(request, user)
                return redirect(request.GET['next'])
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})

@login_required(login_url='/ticker/accounts/login/')
def index(request):
    try:
        active_ticker_length=TickerDetails.objects.all()
        active_ticker=TickerDetails.objects.all().order_by('modified_on').reverse()[:5]

        tmp=active_ticker_length.values_list('ticker_id')
        
        excludedID=[i[0] for i in tmp]

        # for i in tmp:
        #     excludedID.append(i[0])
        start_time=str(date.today())+str(" 00:00:00")
        end_time=str(date.today())+str(" 23:53:53")

        history_ticker_length=TickerHistory.objects.all().filter(is_active=0,is_deleted=1)
        history_ticker=TickerHistory.objects.all().exclude(ticker_id__in=excludedID).filter(is_active=0,is_deleted=1).order_by('modified_on').reverse()[:5]
        today_event=TickerDetails.objects.filter(Q(ticker_start_time__range=(start_time,end_time))
                                                | Q(ticker_end_time__range=(start_time,end_time))
                                                )

        ticker_details={
            'active':len(active_ticker_length),
            'history':len(history_ticker_length),
            'total':(len(history_ticker_length)+len(active_ticker_length)),
            'events': len(today_event),
            'active_ticker_data':active_ticker,
            'history_ticker_data':history_ticker,
            'user':request.user.username
        }
        return render(request, 'index.html',ticker_details)
    except Exception as err:
        logger.error(err)
        return render(request,'acknowledgement.html',{"message":err})

@login_required(login_url='/ticker/accounts/login/')
def createTicker(request):
    try:
        syncDVSData()
    except Exception as err:
        logger.error('Error: '+str(err))
        return render(request,'acknowledgement.html',{"message":f'SetUp not set : {err}'})
    
    data = {
            'pos_box':[
                'fullscreen',
                'top-fix-width',
                'top-right',
                'top-left',
                'center',
                'bottom-fix-width',
                'bottom-right',
                'bottom-left'
                ],
                
            'font_style':[
                "English",
                "Hindi",
                "Chinese",
                "Arabic",
                "Japnese",
                "Russian",
                "French",
                "Spanish",
                "Filipino"
                ],

            'font_size':[
                'large',
                'normal',
                'small'
                ],

            'position':[
                'down',
                'up'
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
                'large',
                'normal',
                'small'
                ],
                
            'emergency_ticker_list':[
                'Earthquake',
                'Fire',
                'Active Shooting',
                'General Evacuation',
                'Custom'
                ],

            'priority':[
                'Low',
                'Medium',
                'High',
                'Emergency'
                ],

            'mediaPriority':[
                'Low',
                'Medium',
                'High'
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
    
    if request.method == 'POST':
        dataget=dataSetter(request)
        if dataget['message']=='Success':
            return redirect(index)
        else:
            return render(request,'acknowledgement.html',dataget)
    else:
        try:
            return render(request, 'createticker.html', data)
        except Exception as err:
            logger.error(err)
            return render(request,'acknowledgement.html',{"message":f"SetUp may be wrong: {err}"})

@login_required(login_url='/ticker/accounts/login/')
def updateTicker(request,ticker_id):
    return render(request,'acknowledgement.html',{"message":"Page not found"})

@login_required(login_url='/ticker/accounts/login/')
def active(request):
    try:
        data=TickerDetails.objects.all().filter().values()
        tickerDataList=sorted(data,key=lambda item: item['ticker_id'],reverse=True)
        data={'tickerDataList':tickerDataList,'user':request.user.username}
        return render(request, 'active.html',data)
    except Exception as err:
        logger.error(err)
        return render(request,'acknowledgement.html',{"message":"Ticker does not exists"})

@login_required(login_url='/ticker/accounts/login/')
def scheduled(request):
    eventData = dict()
    events = list()
    try:
        ticker_obj=TickerDetails.objects.values('ticker_id','ticker_title','ticker_start_time','ticker_end_time')
        for item in ticker_obj:
            data = dict()
            data['groupId']=item['ticker_id']
            data['title']=item['ticker_title']
            data['start']=item['ticker_start_time'].strftime('%Y-%m-%dT%H:%M:%S')
            data['end']=item['ticker_end_time'].strftime('%Y-%m-%dT%H:%M:%S')
            events.append(data)
        eventData['events'] = events
        event = json.dumps(eventData,indent = 3)
        with open(f'{BASE_DIR}/static/resources/events.json', 'w') as f:
            f.write(str(event))
        return render(request, 'scheduled.html',{'user':request.user.username, 'events':events})
    except Exception as err:
        logger.error(err)
        return render(request,'acknowledgement.html',{"message":"File not present"})

@login_required(login_url='/ticker/accounts/login/')
def history(request):
    try:
        active_ticker_length=TickerDetails.objects.all()
        tmp=active_ticker_length.values_list('ticker_id')
        excludedID=list()

        for i in tmp:
            excludedID.append(i[0])
        data=TickerHistory.objects.all().values().exclude(ticker_id__in=excludedID)
        tickerDataList=list()
        for item in data:
            tickerDataList.append(item)
        tickerDataList=sorted(tickerDataList,key=lambda item: item['ticker_id'],reverse=True)
        data={'tickerDataList':tickerDataList,'user':request.user.username}
        return render(request, 'history.html',data)
    except Exception as err:
        logger.error(err)
        return render(request,'acknowledgement.html',{"message":err})

@login_required(login_url='/ticker/accounts/login/')
def detail(request, id):
    try:
        ticker_obj=TickerDetails.objects.filter(ticker_id=int(id)).values()
        if ticker_obj.get()['rundeckid']!=None:
            rundeckData=RundeckLog.objects.all().filter(ticker_id=int(id)).values()

            runningTickers=RundeckLog.objects.all().filter(ticker_id=int(id),tickerStatus='running').values()

            for i in runningTickers:
                rundeck_update(i['rundeck_id'])
            
            rundeckLog=sorted(rundeckData,key=lambda item: item['rundeck_id'],reverse=True)
        else:
            rundeckLog=list()
            dictwithoutrundeckid={'rundeck_id': "None", 'ticker_id': ticker_obj.get()['ticker_id'], 'ticker_title': ticker_obj.get()['ticker_title'], 'execution': "pending", 'successfull_nodes':
             "None", 'failed_nodes': 'None', 'tv_status': 'None', 'iPad_status': 'None'}
            rundeckLog.append(dictwithoutrundeckid)
        return render(request, 'tickerdetail.html' ,{'rundeckLog':rundeckLog, 'logObject':list()})
    except Exception as err:
        logger.error('Error: '+str(err))
        return render(request,'acknowledgement.html',{"message":"Ticker ID not present"})
        # return active(request)

@login_required(login_url='/ticker/accounts/login/')
def abort(request,id):
    try:
        ticker_obj=TickerDetails.objects.filter(ticker_id=int(id)).values()
        if ticker_obj.get()['rundeckid']!=None:
            Thread(target=killTicker,args=(ticker_obj,)).start()
            rundeckLogData=RundeckLog.objects.all().filter(ticker_id=int(id)).values()
            rundeckLog=sorted(rundeckLogData,key=lambda item: item['rundeck_id'],reverse=True)
        
        TickerDetails.objects.filter(ticker_id=int(id),frequency='1').values().update(ticker_end_time=datetime.now(),is_active=0,is_deleted=1)

        return render(request, 'tickerdetail.html' ,{'rundeckLog':rundeckLog})#, 'logObject':logObject})
    except Exception as err:
        return render(request,'acknowledgement.html',{"message":err})

@login_required(login_url='/ticker/accounts/login/')
def isEdit(request, id):
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
            'down',
            'up'
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
            'Low',
            'Emergency'
            ],

        'mediaPriority':[
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
    tickerObj=TickerDetails.objects.filter(ticker_id=int(id)).values()
    data['tickerObj'] = tickerObj.get()
    return render(request, 'createticker.html',data)

@login_required(login_url='/ticker/accounts/login/')
def isRestore(request):
    pass

@login_required(login_url='/ticker/accounts/login/')
def isDelete(request, id):
    try:
        tickerDataDelete = TickerDetails.objects.filter(ticker_id=id)
        ticker_json=json.loads(tickerDataDelete.values().get().get('ticker_json'))
        if ticker_json.get('main_ticker_condition','not found')==True and ticker_json.get('main_ticker_logo','not found')==True:
            image_name=ticker_json.get('main_ticker_logo_name')
        elif ticker_json.get('static_ticker_condition','not found')==True and ticker_json.get('static_ticker_logo','not found')==True:
            image_name=ticker_json.get('static_ticker_logo_name')
        elif ticker_json.get('moving_ticker_condition','not found')==True:
            image_name=ticker_json.get('moving_ticker_logo_name')
        elif  ticker_json.get('emergency_ticker_condition','not found')==True:
            image_name=ticker_json.get('emergency_ticker_logo_name')
    except Exception  as e:
        logger.error(f'ID {id} not found')
        return render(request,'acknowledgement.html',{"message":'Specificied ID not found'})
            # messages.info(request, 'Specificied ID not found')
            # return redirect(active)
    try:
        os.remove(FileSystemStorage().base_location+str('/')+image_name.split('/')[-1])
    except Exception as err:
        logger.info(f'No image found for {id} ticker id')
    try:
        tickerDataDelete.delete()
        return redirect(active)
    except Exception as err:
        logger.error(f'Unable to delete {id} ID')
        return render(request,'acknowledgement.html',{"message":'Unable to delete specificied ID'})
       
@login_required(login_url='/ticker/accounts/login/')
def isDeleteHistory(request, id):
    try:
            tickerDataDelete = TickerHistory.objects.filter(ticker_id=id)
            ticker_json=json.loads(tickerDataDelete.values().get().get('ticker_json'))
            if ticker_json.get('main_ticker_condition','not found')==True and ticker_json.get('main_ticker_logo','not found')==True:
                image_name=ticker_json.get('main_ticker_logo_name')
            elif ticker_json.get('static_ticker_condition','not found')==True and ticker_json.get('static_ticker_logo','not found')==True:
                image_name=ticker_json.get('static_ticker_logo_name')
            elif ticker_json.get('moving_ticker_condition','not found')==True:
                image_name=ticker_json.get('moving_ticker_logo_name')
            elif  ticker_json.get('emergency_ticker_condition','not found')==True:
                image_name=ticker_json.get('emergency_ticker_logo_name')
    except TickerHistory.DoesNotExist  as e:
        logger.error(f'ID {id} not found')
        return render(request,'acknowledgement.html',{"message":'Specificied ID not found'})

    try:
        os.remove(FileSystemStorage().base_location+str('/')+image_name.split('/')[-1])
    except Exception as err:
        logger.info(f'No image found for {id} ticker id')
    
    try:
        tickerDataDelete.delete()
        return redirect(history)
    except Exception as err:
        logger.error(f'Unable to delete {id} ID. ERROR: '+str(err))
        return render(request,'acknowledgement.html',{"message":'Unable to delete specificied ID'})

@login_required(login_url='/ticker/accounts/login/')
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
    except Exception as err:
        return render(request,'acknowledgement.html',{"message":err})

# def avDataFilter():
#     try:
#         file=open(f'{str(BASE_DIR)}/static/resources/resourceAV.json')
#         file=json.load(file)

#         data=set()

#         for item in file['data']:
#             data.add(item['key_id'])

#         data=list(data)

#         file=open(f'{str(BASE_DIR)}/static/resources/resource.json')
#         file=json.load(file)

#         count=0

#         for item in file['data']:
#             if item['id'] not in data:
#                 count+=1
#                 file['data'].remove(item)

#         filteredData=json.dumps(file,indent=3)

#         logger.info(str(count)+" AV data filtered")

#         with open(f'{str(BASE_DIR)}/static/resources/resource.json','w') as file:
#             file.write(filteredData)
#     except Exception as err:
#         logger.error(err)

def dataFilter(filePath):
    avFile=json.load(open(filePath+'resourceAV.json'))
    resourceXml=XMLReader.parse(filePath+'resource.xml').getroot()
    mainFile=json.load(open(filePath+'resource.json'))

    avList=list()
    xmlList=list()
    mainList=list()
    mainDict=dict()

    for item in avFile['data']:
        avList.append(item['key_id'])   

    avList=set(avList)

    for child in resourceXml:
        if child.get('key_id'):
            xmlList.append(child.get('key_id'))

    xmlList=set(xmlList)
    
    filteredList=avList.intersection(xmlList)
    
    for keys in mainFile.keys():
        if keys=='data':
            pass
        else:
            mainDict[keys]=mainFile[keys]

    for item in mainFile['data']:
        if item['id'] in filteredList:
            mainList.append(item)

    mainDict['data']=mainList

    mainFile=json.dumps(mainDict,indent=3)

    with open(str(filePath+'resource.json'),'w+') as file:
        file.write(mainFile)
    logger.info('Filtered data')

def syncDVSData():
    try:
        dvs_data=SetUp.objects.filter(id=1).values()
        FQDN=dvs_data.get()['FQDN']
        Dvs_Token=dvs_data.get()['Dvs_Token']
        
        headers = {
            'Content-Type': 'application/vnd.digivalet.v1+json',
            'Access-Token': Dvs_Token,
        }

        data = '{}'

        baseFQDN=f'https://{FQDN}/dvs/'
        filePath=f'{str(BASE_DIR)}/static/resources/'
    except Exception as err:
        raise

    try:
        response = requests.post(baseFQDN+'api/key/selectR', headers=headers, data=data)
        response=json.dumps(response.json(),indent=3).encode('utf-8')
        with open((str(filePath)+'resource.json'),'wb') as file:
            file.write(response)
        
        headers = {
        'Content-Type': 'application/vnd.digivalet.v1+json',
        'Access-Token': 'da1ca0a34d72bd530bfc21b7a4d70ec903a0611c18058eb8b6290cae6644251e',
        }

        data = '{"device_type_id": "2"}'

        response = requests.post(baseFQDN+'api/inRoomDevice/selectR', headers=headers, data=data)
        response=json.dumps(response.json(),indent=3).encode('utf-8')
        with open((str(filePath)+'resourceAV.json'),'wb') as file:
            file.write(response)

        response = requests.get(baseFQDN+'core/resourcexml')
        response=response.text.encode('utf-8')
        with open((str(filePath)+'resource.xml'),'wb') as file:
            file.write(response)
    except Exception as err:
        logger.error("Api call error: "+str(err))
        raise
    try:
        Thread(target=dataFilter,args=(filePath,)).start()
    except:
        raise

# def filterData():
#     DVSDATA = dict()
#     roomTypeData = set()
#     wingData = set()
#     floorData = set()
#     keyData = set()
#     xmlDocument = XMLReader.parse(f"{BASE_DIR}/static/resources/resource.xml").getroot()
#     for item in xmlDocument.findall('node'):
#         if item.get('room_type') != None:
#             roomTypeData.add(item.get('room_type'))
#         if item.get('floor') != None:
#             floorData.add(item.get('floor'))
#         if item.get('key_no') != None:
#             keyData.add(item.get('key_no'))
    
#     jsonDocument = json.load(open(f"{BASE_DIR}/static/resources/resource.json"))
#     for item in jsonDocument:
#         wingData.add(item.get('wing_name'))
#     DVSDATA["roomType"]=sorted(roomTypeData)
#     DVSDATA["wing"] = sorted(wingData)
#     DVSDATA["floor"] = sorted(floorData)
#     DVSDATA["key"] = sorted(keyData)
#     return DVSDATA

@api_view(['GET', 'POST', 'DELETE'])
def taskPost(request,id="0"):
    logger.info('TaskPost Api hitted')
    if request.method == 'POST':
        d=dict()
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
        serializer = TaskSerializerConfig(data=request.data)
        p=serializer.initial_data
        q=int(p.get('ticker_id'))
        ticker_obj = TickerDetails.objects.filter(ticker_id=q).values()
        if (ticker_obj.get()['ticker_end_time'])<datetime.now() and (ticker_obj.get()['ticker_type']=="Emergency Ticker"):
            Content={"Completed":True}
        else:
            Content={"Completed:":False}
        return Response(Content)

    elif request.method == 'DELETE':
        serializer = TaskSerializer(data=request.data)
        p=serializer.initial_data
        q=int(p['id'])
        task = Task.objects.get(id=q)
        task.delete()
        return Response('Item succsesfully delete!')


#### TICKER CONFIG SECTION START ####
@api_view(['GET'])
def configApi(request,pk="0"):
    logger.info('Config Api hitted')
    if request.method == 'GET':

        try:
            if request.headers.get('tickerToken') == None:
                res['status'] = False
                res['statusCode'] = tokenPresent.get('statusCode')
                res['message'] = tokenPresent.get('message')

                logger.info(tokenPresent.get('message'))
                return Response(res, status = status.HTTP_401_UNAUTHORIZED)

            else:

                if tokenValidation(request.headers.get('tickerToken')):
                    serializer = TaskSerializerConfig(data=request.data)
                    p=serializer.initial_data

                    q=int(p.get('ticker_id'))

                    if TickerDetails.objects.filter(ticker_id=q).exists() or TickerHistory.objects.filter(ticker_id=q).exists():

                        try:

                            tasks = TickerDetails.objects.filter(ticker_id=q).values_list('ticker_json','ticker_end_time','frequency')
                            ticker_config_file = json.loads(tasks.get()[0])

                            # if tasks.get()[2]=='1':
                            #     time_interval=tasks.get()[1]-datetime.now()
                            #     time_interval=time_interval.total_seconds()
                            #     if time_interval>0:
                            #         ticker_config_file['time_interval']=int(time_interval)
                            #     else:
                            #         ticker_config_file['time_interval'] =0

                            try:
                                ticker_config_file['auth_token'] = AUTH_TOKEN_API

                            except:
                                ticker_config_file['auth_token'] = "YWRtaW46YWRtaW4xMjM0"
                            
                            tasks = json.dumps(ticker_config_file,indent=3)

                            return Response(json.loads(tasks))

                        except TickerDetails.DoesNotExist as err:


                            tasks=TickerHistory.objects.filter(ticker_id=q).values_list('ticker_json','ticker_end_time','frequency')
                            ticker_config_file = json.loads(tasks.get()[0])

                            # if tasks.get()[2]=='1':
                            #     time_interval=tasks.get()[1]-datetime.now()
                            #     time_interval=time_interval.total_seconds()
                            #     print(time_interval)
                            #     if time_interval>0:
                            #         ticker_config_file['time_interval']=int(time_interval)
                            #     else:
                            #         ticker_config_file['time_interval'] = 0

                            try:
                                ticker_config_file['auth_token'] = AUTH_TOKEN_API
                                
                            except:
                                ticker_config_file['auth_token'] = "YWRtaW46YWRtaW4xMjM0"
                            
                            # print(tasks['ticker_end_time'],type(tasks['ticker_end_time']))

                            # ticker_config_file['time_interval']=int()

                            logger.info("Fetched from TickerHistory as "+str(err))

                            tasks = json.dumps(ticker_config_file,indent=3)
                            return Response(json.loads(tasks))
                    
                    else:
                        
                        res['status'] = False
                        res['statusCode'] = ConfigNotFoundFailure.get('statusCode')
                        res['message'] = ConfigNotFoundFailure.get('message')

                        logger.info(ConfigNotFoundFailure.get('message'))
                        return Response(res, status = status.HTTP_401_UNAUTHORIZED) 
                else:

                        res['status'] = False
                        res['statusCode'] = tokenFailure.get('statusCode')
                        res['message'] = tokenFailure.get('message')

                        logger.info(tokenFailure.get('message'))
                        return Response(res, status = status.HTTP_401_UNAUTHORIZED)   

        except Exception as err:

            res['status'] = False
            res['statusCode'] = ConfigFailure.get('statusCode')
            res['message'] = ConfigFailure.get('message')

            logger.info(ConfigFailure.get('message'))
            logger.error(err)
            return Response(res, status = status.HTTP_404_NOT_FOUND)
         
    else:

        res['status'] = False
        res['statusCode'] = requestInvalid.get('statusCode')
        res['message'] = requestInvalid.get('message')

        logger.info(requestInvalid.get('message'))
        return Response(res, status = status.HTTP_404_NOT_FOUND)
#### TICKER CONFIG SECTION END ####


#### MAIL SET-UP SECTION START ####
def setupMail():
    try:

        subject = "Hello"
        body = ""
        emailQueue = ['temper.projectgroup@gmail.com']
        email = EmailMessage(subject, body, to=emailQueue)
        email.send()

    except Exception as err:
        pass
#### MAIL SET-UP SECTION END ####


#### TOKEN VALIDATION SECTION START ####
def tokenValidation(token):
    if token == AUTH_TOKEN_API:
        return True
    # return True
    return False
#### TOKEN VALIDATION SECTION END ####


#### IP VALIDATION SECTION START ####
def ipAddressValidation(ip):
    ip_address_validate_pattern = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    check_fun = re.match(ip_address_validate_pattern, ip)
    if check_fun:
        return True
    return False
#### IP VALIDATION SECTION END ####


#### REBOOT STATUS SECTION START ####
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def rebootStatus(request):
    if request.method=='GET':

        try:
            if request.headers.get('tickerToken') == None:

                res['status'] = False
                res['statusCode'] = tokenPresent.get('statusCode')
                res['message'] = tokenPresent.get('message')

                logger.info(tokenPresent.get('message'))
                return Response(res, status = status.HTTP_401_UNAUTHORIZED)

            else:

                try:
                    if tokenValidation(request.headers.get('tickerToken')):

                        if request.GET.get('dvcIp') != None:

                            if ipAddressValidation(request.GET.get('dvcIp')):

                                try:
                                    tickerDetailsDB=TickerDetails.objects.all().filter(ticker_start_time__lte=datetime.now(),ticker_end_time__gt=datetime.now()).values()
                                    # print(tickerDetailsDB)
                                    if len(tickerDetailsDB)>0:

                                        data=getTickerId(tickerDetailsDB,request.GET.get('dvcIp'))

                                        print(data)

                                        if data['ticker_id']==-1 or data['key_name']=='Not Found':

                                            res['status'] = False
                                            res['statusCode'] = rebootNodeNotFound.get('statusCode')
                                            res['message'] = rebootNodeNotFound.get('message')

                                            logger.info(rebootNodeNotFound.get('message'))
                                            return Response(res)

                                        else:
                                            try:

                                                try:
                                                    auth=AUTH_TOKEN_API
                                                except:
                                                    auth="YWRtaW46YWRtaW4xMjM0"
                                                
                                                setup=SetUp.objects.filter(id=1).values()

                                                FQDN=setup.get()['FQDN']
                                                Dvs_Token=setup.get()['Dvs_Token']
                                                Rundeck_Token=setup.get()['Rundeck_Token']
                                                Rundeck_Api_Version=setup.get()['Rundeck_Api_Version']
                                                Ticker_FQDN=setup.get()['Ticker_FQDN']
                                                Rundeck_Start_Job=setup.get()['Rundeck_Start_Job']

                                                basicTickerInfo={
                                                    'FQDN':FQDN,
                                                    'Dvs_Token':Dvs_Token,
                                                    'Rundeck_Token':Rundeck_Token,
                                                    'Rundeck_Api_Version':Rundeck_Api_Version,
                                                    'Ticker_FQDN':Ticker_FQDN,
                                                    'Rundeck_Start_Job':Rundeck_Start_Job
                                                }
                                                
                                                json_data = {
                                                    'argString': f"-whichnode {data['key_name']} -FQDN {Ticker_FQDN} -jsonFile {data['ticker_id']} -BasicAuth {auth}",
                                                }

                                                basicTickerInfo['json_data']=json_data

                                                print(basicTickerInfo['json_data'])

                                                ticker_obj=TickerDetails.objects.filter(ticker_id=data['ticker_id']).values()

                                                ticker_id=ticker_obj.get()['ticker_id']
                                                callscheduledticker.apply_async(args=[basicTickerInfo,ticker_id,-1])

                                                res['status'] = True
                                                res['statusCode'] = rebootSuccessStatus.get('statusCode')
                                                res['message'] = rebootSuccessStatus.get('message')

                                                logger.info(rebootSuccessStatus.get('message'))
                                                return Response(res)

                                            except Exception as err:
                                                
                                                res['status'] = False
                                                res['statusCode'] = rebootNotReschedule.get('statusCode')
                                                res['message'] = rebootNotReschedule.get('message')

                                                logger.info(rebootNotReschedule.get('message'))
                                                logger.error(err)
                                                return Response(res)
                                                
                                    else:

                                        res['status'] = False
                                        res['statusCode'] = rebootFailureStatus.get('statusCode')
                                        res['message'] = rebootFailureStatus.get('message')

                                        logger.info(rebootFailureStatus.get('message'))
                                        return Response(res)

                                except Exception as err:
                                    
                                    res['status'] = False
                                    res['statusCode'] = DBError.get('statusCode')
                                    res['message'] = DBError.get('message')

                                    logger.info(DBError.get('message'))
                                    logger.error(err)
                                    return Response(res)

                            else:

                                res['status'] = False
                                res['statusCode'] = ipAddressFailure.get('statusCode')
                                res['message'] = ipAddressFailure.get('message')

                                logger.info(ipAddressFailure.get('message'))
                                return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                        else:

                            res['status'] = False
                            res['statusCode'] = ipAddressPresent.get('statusCode')
                            res['message'] = ipAddressPresent.get('message')
                            
                            logger.info(ipAddressPresent.get('message'))
                            return Response(res)

                    else:

                        res['status'] = False
                        res['statusCode'] = tokenFailure.get('statusCode')
                        res['message'] = tokenFailure.get('message')

                        logger.info(tokenFailure.get('message'))
                        return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                except Exception as err:

                    res['status'] = False
                    res['statusCode'] = validationError.get('statusCode')
                    res['message'] = validationError.get('message')

                    logger.info(validationError.get('message'))
                    logger.error(err)
                    return Response(res)

        except Exception as err:

            res['status'] = False
            res['statusCode'] = rebootStatusError.get('statusCode')
            res['message'] = rebootStatusError.get('message')

            logger.info(rebootStatusError.get('message'))
            logger.error(err)
            return Response(res)

    else:

        res['status'] = False
        res['statusCode'] = requestInvalid.get('statusCode')
        res['message'] = requestInvalid.get('message')

        logger.info(requestInvalid.get('message'))
        return Response(res)
#### REBOOT STATUS SECTION END ####


#### TV IPAD STATUS SECTION START ####
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def tvIpadStatus(request):
    if request.method=='POST':

        try:
            if request.headers.get('tickerToken') == None:

                res['status'] = False
                res['statusCode'] = tokenPresent.get('statusCode')
                res['message'] = tokenPresent.get('message')

                logger.info(tokenPresent.get('message'))
                return Response(res, status = status.HTTP_401_UNAUTHORIZED)

            else:
                try:
                    if tokenValidation(request.headers.get('tickerToken')):

                        if request.body != b'':

                            tvIpadStatusData=json.loads(request.body.decode('utf-8'))

                            dvcIp=tvIpadStatusData.get('dvcIp')
                            ipadStatus=tvIpadStatusData.get('ipadStatus')
                            tvStatus=tvIpadStatusData.get('tvStatus')

                            print(dvcIp,ipadStatus,tvStatus)

                            if dvcIp==None or ipadStatus==None or tvStatus==None:
                                print('s')

                                res['status'] = False
                                res['statusCode'] = dataNotFound.get('statusCode')
                                res['message'] = dataNotFound.get('message')

                                logger.info(dataNotFound.get('message'))
                                return Response(res)

                            else:
                                try:

                                    nowTime=datetime.now()
                                    tickerDetailsDB=TickerDetails.objects.all().filter(ticker_start_time__lte=nowTime,ticker_end_time__gt=nowTime).values()

                                    if len(tickerDetailsDB)>0:
                                        data=getTickerId(tickerDetailsDB,dvcIp)
                                        
                                        if data['key_name']=="Not Found":

                                            res['status'] = False
                                            res['statusCode'] = dvcNotFound.get('statusCode')
                                            res['message'] = dvcNotFound.get('message')

                                            logger.info(dvcNotFound.get('message'))
                                            return Response(res)
                                            
                                        else:

                                            rundeckLogDB=RundeckLog.objects.filter(ticker_id=int(data['ticker_id'])).values()
                                            tv_status=rundeckLogDB.get()['tv_status'].strip('[]')
                                            iPad_status=rundeckLogDB.get()['iPad_status'].strip('[]')

                                            tvStatusList=list()
                                            ipadStatusList=list()
                                                                                       
                                            tvStatusList.append({data['key_name']:str(tvStatus)})
                                                                                        
                                            ipadStatusList.append({data['key_name']:str(ipadStatus)})
                                            
                                            if len(tv_status)>0 and tv_status!='None':
                                                removeDuplicate(tvStatusList,tv_status)
                                            if len(iPad_status)>0 and iPad_status!='None':
                                                removeDuplicate(ipadStatusList,iPad_status)

                                            print(tvStatusList,ipadStatusList)

                                            rundeckLogDB.update(tv_status=tvStatusList,iPad_status=ipadStatusList)

                                            res['status'] = True
                                            res['statusCode'] = tvIpadSuccessStatus.get('statusCode')
                                            res['message'] = tvIpadSuccessStatus.get('message')

                                            logger.info(tvIpadSuccessStatus.get('message'))
                                            return Response(res)
                                    else:

                                        res['status'] = False
                                        res['statusCode'] = tickerNotFound.get('statusCode')
                                        res['message'] = tickerNotFound.get('message')

                                        logger.info(tickerNotFound.get('message'))
                                        return Response(res)

                                except Exception as err:
                                    res['status'] = False
                                    res['statusCode'] = DBError.get('statusCode')
                                    res['message'] = DBError.get('message')

                                    logger.info(DBError.get('message'))
                                    logger.error(err)
                                    return Response(res)
                            
                        else:

                            res['status'] = False
                            res['statusCode'] = requestBody.get('statusCode')
                            res['message'] = requestBody.get('message')

                            logger.info(requestBody.get('message'))
                            return Response(res)
                            
                    else:

                        res['status'] = False
                        res['statusCode'] = tokenFailure.get('statusCode')
                        res['message'] = tokenFailure.get('message')

                        logger.info(tokenFailure.get('message'))
                        return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                except Exception as err:

                    res['status'] = False
                    res['statusCode'] = validationError.get('statusCode')
                    res['message'] = validationError.get('message')

                    logger.info(validationError.get('message'))
                    logger.error(err)
                    return Response(res)

        except Exception as err:

            res['status'] = False
            res['statusCode'] = tvIpadStatusError.get('statusCode')
            res['message'] = tvIpadStatusError.get('message')
            res['data'] = None

            logger.info(tvIpadStatusError.get('message'))
            logger.error(err)
            return Response(res)

    else:

        res['status'] = False
        res['statusCode'] = requestInvalid.get('statusCode')
        res['message'] = requestInvalid.get('message')

        logger.info(requestInvalid.get('message'))
        return Response(res)
#### TV IPAD STATUS SECTION END ####


####  TICKER CLOSE STATUS SECTION START ####
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def statusClose(request):
    logger.info('statusClose api hitted')
    if request.method=='POST':

        try:
            if request.body != b'':
                statusCloseData = request.body

                if request.headers.get('tickerToken') == None:

                    res['status'] = False
                    res['statusCode'] = tokenPresent.get('statusCode')
                    res['message'] = tokenPresent.get('message')

                    logger.info(tokenPresent.get('message'))
                    return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                else:
                    try:
                        if tokenValidation(request.headers.get('tickerToken')):

                            statusCloseData=json.loads(request.body.decode('utf-8'))

                            if statusCloseData.get('dvcIp') != None:

                                if ipAddressValidation(statusCloseData.get('dvcIp')):

                                    try:

                                        #### Start code here ####
                                        
                                        res['status'] = True
                                        res['statusCode'] = tickerCloseStatus.get('statusCode')
                                        res['message'] = tickerCloseStatus.get('message')

                                        logger.info(tickerCloseStatus.get('message'))
                                        return Response(res)

                                    except Exception as err:

                                        res['status'] = False
                                        res['statusCode'] = DBError.get('statusCode')
                                        res['message'] = DBError.get('message')

                                        logger.info(DBError.get('message'))
                                        logger.error(err)
                                        return Response(res)

                                else:

                                    res['status'] = False
                                    res['statusCode'] = ipAddressFailure.get('statusCode')
                                    res['message'] = ipAddressFailure.get('message')

                                    logger.info(ipAddressFailure.get('message'))
                                    return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                            else:

                                res['status'] = False
                                res['statusCode'] = ipAddressPresent.get('statusCode')
                                res['message'] = ipAddressPresent.get('message')
                                
                                logger.info(ipAddressPresent.get('message'))
                                return Response(res)

                        else:
                            
                            res['status'] = False
                            res['statusCode'] = tokenFailure.get('statusCode')
                            res['message'] = tokenFailure.get('message')

                            logger.info(tokenFailure.get('message'))
                            return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                    except Exception as err:

                        res['status'] = False
                        res['statusCode'] = validationError.get('statusCode')
                        res['message'] = validationError.get('message')

                        logger.info(validationError.get('message'))
                        logger.error(err)
                        return Response(res)
            else:

                res['status'] = False
                res['statusCode'] = requestBody.get('statusCode')
                res['message'] = requestBody.get('message')
                
                logger.info(requestBody.get('message'))
                return Response(res)

        except Exception as err:

            res['status'] = False
            res['statusCode'] = TickerCloseError.get('statusCode')
            res['message'] = TickerCloseError.get('message')

            logger.info(TickerCloseError.get('message'))
            logger.error(err)
            return Response(res)

    else:

        res['status'] = False
        res['statusCode'] = requestInvalid.get('statusCode')
        res['message'] = requestInvalid.get('message')

        logger.info(requestInvalid.get('message'))
        return Response(res)
####  TICKER CLOSE STATUS SECTION END ####


####  TICKER DND STATUS SECTION START ####
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def dndStatus(request):
    logger.info('statusClose api hitted')
    if request.method=='POST':

        try:
            if request.body != b'':
                statusCloseData = request.body

                if request.headers.get('tickerToken') == None:

                    res['status'] = False
                    res['statusCode'] = tokenPresent.get('statusCode')
                    res['message'] = tokenPresent.get('message')

                    logger.info(tokenPresent.get('message'))
                    return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                else:
                    try:
                        if tokenValidation(request.headers.get('tickerToken')):

                            dndStatusData=json.loads(request.body.decode('utf-8'))

                            if dndStatusData.get('dvcIp') != None:

                                if ipAddressValidation(dndStatusData.get('dvcIp')):

                                    try:

                                        #### Start code here ####

                                        res['status'] = True
                                        res['statusCode'] = tickerCloseStatus.get('statusCode')
                                        res['message'] = tickerCloseStatus.get('message')

                                        logger.info(tickerCloseStatus.get('message'))
                                        return Response(res)

                                    except Exception as err:

                                        res['status'] = False
                                        res['statusCode'] = DBError.get('statusCode')
                                        res['message'] = DBError.get('message')

                                        logger.info(DBError.get('message'))
                                        logger.error(err)
                                        return Response(res)

                                else:

                                    res['status'] = False
                                    res['statusCode'] = ipAddressFailure.get('statusCode')
                                    res['message'] = ipAddressFailure.get('message')

                                    logger.info(ipAddressFailure.get('message'))
                                    return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                            else:

                                res['status'] = False
                                res['statusCode'] = ipAddressPresent.get('statusCode')
                                res['message'] = ipAddressPresent.get('message')
                                
                                logger.info(ipAddressPresent.get('message'))
                                return Response(res)

                        else:
                            
                            res['status'] = False
                            res['statusCode'] = tokenFailure.get('statusCode')
                            res['message'] = tokenFailure.get('message')

                            logger.info(tokenFailure.get('message'))
                            return Response(res, status = status.HTTP_401_UNAUTHORIZED)

                    except Exception as err:

                        res['status'] = False
                        res['statusCode'] = validationError.get('statusCode')
                        res['message'] = validationError.get('message')

                        logger.info(validationError.get('message'))
                        logger.error(err)
                        return Response(res)
            else:

                res['status'] = False
                res['statusCode'] = requestBody.get('statusCode')
                res['message'] = requestBody.get('message')
                
                logger.info(requestBody.get('message'))
                return Response(res)

        except Exception as err:

            res['status'] = False
            res['statusCode'] = dndStatusError.get('statusCode')
            res['message'] = dndStatusError.get('message')

            logger.info(dndStatusError.get('message'))
            logger.error(err)
            return Response(res)

    else:

        res['status'] = False
        res['statusCode'] = requestInvalid.get('statusCode')
        res['message'] = requestInvalid.get('message')

        logger.info(requestInvalid.get('message'))
        return Response(res)
####  TICKER DND STATUS SECTION END ####


#### CHECK PRIORITY TICKER SECTION START ####
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def checkPriorityTicker(request):
    if request.method=='POST':

        try:
            if request.body != b'':

                bodyData=json.loads(request.body.decode('utf-8'))
                
                if bodyData['tickerToken'] == None:

                    resp['status'] = False
                    resp['statusCode'] = tokenPresent.get('statusCode')
                    resp['message'] = tokenPresent.get('message')
                    resp['data'] = None

                    logger.info(tokenPresent.get('message'))
                    return Response(resp, status = status.HTTP_401_UNAUTHORIZED)

                else:
                    try:
                        if tokenValidation(bodyData['tickerToken']):

                            mainData=checkPriority(bodyData['newTickerPriority'],bodyData['wings'],bodyData['floors'],bodyData['rooms'],bodyData['startTime'],bodyData['endTime'],bodyData['timeInterval'])

                            resp['status'] = True
                            resp['statusCode'] = priorityTickerAPISuccess.get('statusCode')
                            resp['message'] = priorityTickerAPISuccess.get('message')
                            resp['data'] = {"message": mainData['runningTicker']['message'],"runningTickerID": mainData['runningTickerID']}

                            logger.info(priorityTickerAPISuccess.get('message'))
                            return Response(resp)

                        else:
                            
                            resp['status'] = False
                            resp['statusCode'] = tokenFailure.get('statusCode')
                            resp['message'] = tokenFailure.get('message')
                            resp['data'] = None

                            logger.info(tokenFailure.get('message'))
                            return Response(resp, status = status.HTTP_401_UNAUTHORIZED)

                    except Exception as err:

                        resp['status'] = False
                        resp['statusCode'] = validationError.get('statusCode')
                        resp['message'] = validationError.get('message')
                        resp['data'] = None

                        logger.info(validationError.get('message'))
                        logger.error(err)
                        return Response(resp)
            else:

                resp['status'] = False
                resp['statusCode'] = requestBody.get('statusCode')
                resp['message'] = requestBody.get('message')
                resp['data'] = None
                
                logger.info(requestBody.get('message'))
                return Response(resp)

        except Exception as err:

            resp['status'] = False
            resp['statusCode'] = priorityTickerAPIFailure.get('statusCode')
            resp['message'] = priorityTickerAPIFailure.get('message')
            resp['data'] = None

            logger.info(priorityTickerAPIFailure.get('message'))
            logger.error(err)
            return Response(resp)

    else:

        resp['status'] = False
        resp['statusCode'] = requestInvalid.get('statusCode')
        resp['message'] = requestInvalid.get('message')
        resp['data'] = None

        logger.info(requestInvalid.get('message'))
        return Response(resp)
#### CHECK PRIORITY TICKER SECTION STOP ####


#### REMOVE TICKER SECTION START ####
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def closeTicker(request):
    if request.method=='POST':
        try:
            if request.body != b'':


                bodyData=json.loads(request.body.decode('utf-8'))
                
                if bodyData['tickerToken'] == None:

                    resp['status'] = False
                    resp['statusCode'] = tokenPresent.get('statusCode')
                    resp['message'] = tokenPresent.get('message')
                    resp['data'] = None

                    logger.info(tokenPresent.get('message'))
                    return Response(resp, status = status.HTTP_401_UNAUTHORIZED)

                else:
                    try:
                        if tokenValidation(bodyData['tickerToken']):

                            #### Write code here ####
                            resp['status'] = True
                            resp['statusCode'] = closeTickerAPISuccess.get('statusCode')
                            resp['message'] = closeTickerAPISuccess.get('message')
                            resp['data'] = None

                            logger.info(closeTickerAPISuccess.get('message'))
                            return Response(resp)
                           
                        else:
                            
                            resp['status'] = False
                            resp['statusCode'] = tokenFailure.get('statusCode')
                            resp['message'] = tokenFailure.get('message')
                            resp['data'] = None

                            logger.info(tokenFailure.get('message'))
                            return Response(resp, status = status.HTTP_401_UNAUTHORIZED)

                    except Exception as err:

                        resp['status'] = False
                        resp['statusCode'] = validationError.get('statusCode')
                        resp['message'] = validationError.get('message')
                        resp['data'] = None

                        logger.info(validationError.get('message'))
                        logger.error(err)
                        return Response(resp)
                        
            else:

                resp['status'] = False
                resp['statusCode'] = requestBody.get('statusCode')
                resp['message'] = requestBody.get('message')
                resp['data'] = None
                
                logger.info(requestBody.get('message'))
                return Response(resp)

        except Exception as err:

            resp['status'] = False
            resp['statusCode'] = closeTickerAPIFailure.get('statusCode')
            resp['message'] = closeTickerAPIFailure.get('message')
            resp['data'] = None

            logger.info(closeTickerAPIFailure.get('message'))
            logger.error(err)
            return Response(resp)

    else:

        resp['status'] = False
        resp['statusCode'] = requestInvalid.get('statusCode')
        resp['message'] = requestInvalid.get('message')
        resp['data'] = None

        logger.info(requestInvalid.get('message'))
        return Response(resp)
#### REMOVE TICKER SECTION STOP ####


#### Dashboard Sys Log Section Start ####
@login_required(login_url='/ticker/accounts/login/')
def systemLog(request):
    context = dict()

    try:
        sysLog = list()
        with open('logs/info.log') as file:
            for line in (file.readlines() [-20:]):
                sysLog.append(line)
         
        context['segment'] = 'info'
        context['sysLog'] = sysLog

        return render(request, 'systemLogs.html', context)

    except Exception as err:

        logger.info(templateError.get('message'))
        logger.error(err)
        return render(request,'acknowledgement.html', {"message":err})
#### Dashboard Sys Log Section End ####



#### Dashboard Celery Beat Log Section Start ####
@login_required(login_url='/ticker/accounts/login/')
def celeryBeatLog(request):
    context = dict()

    try:
        sysLog = list()
        with open('logs/celery_beat_info.log') as file:
            for line in (file.readlines() [-20:]):
                sysLog.append(line)
         
        context['segment'] = 'beat'
        context['sysLog'] = sysLog

        return render(request, 'systemLogs.html', context)

    except Exception as err:

        logger.info(templateError.get('message'))
        logger.error(err)
        return render(request,'acknowledgement.html', {"message":err})
#### Dashboard Celery Beat Log Section End ####



#### Dashboard Celery Worker Log Section Start ####
@login_required(login_url='/ticker/accounts/login/')
def celeryWorkerLog(request):
    context = dict()

    try:
        sysLog = list()
        with open('logs/celery_worker_info.log') as file:
            for line in (file.readlines() [-40:]):
                sysLog.append(line)
        
        context['segment'] = 'worker'
        context['sysLog'] = sysLog

        return render(request, 'systemLogs.html', context)

    except Exception  as err:

        logger.info(templateError.get('message'))
        logger.error(err)
        return render(request,'acknowledgement.html', {"message":err})
#### Dashboard Celery Worker Log Section End ####