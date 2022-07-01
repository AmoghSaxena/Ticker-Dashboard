from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from ticker_management.gadget import datagetter,filterData, schedulingdata
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from datetime import datetime
from ticker_management.models import TickerDetails,TickerHistory
from ticker_management.tasks import test_fun

from .forms import LoginForm


#Api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from rest_framework.response import Response
from .models import Task
#Api


@login_required
def index(request):

    active_ticker=TickerDetails.objects.all().filter(is_active=1)
    total_ticker=TickerHistory.objects.all()

    ticker_count={
        'active':len(active_ticker),
        'pending':8,
        'total':len(total_ticker)+len(active_ticker)
    }

    return render(request, 'index.html',ticker_count)

@login_required
def createticker(request):

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
                'left',
                'right'
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
            ]
        }
    
    if request.method == 'POST':
        if (
            request.POST.get('static_ticker_enabler')=='' or 
            request.POST.get('primary_ticker_enabler')=='' or 
            request.POST.get('secondary_ticker_enabler')=='' or 
            request.POST.get('animation_ticker_enabler')=='' or 
            request.POST.get('emergency_ticker_enabler')==''
           ):
            return redirect(preview,id=datagetter(request).get('ticker_id'))
        else:
            return render(request, 'createticker.html', data)
    else:
        return render(request, 'createticker.html', data)

@login_required
def active(request):

    t=TickerDetails.objects.all().filter(is_active=1).values()

    tickerdatalist=list()
    for a in t:
        tickerdatalist.append(a)
    
    tickerdatalist=sorted(tickerdatalist,key=lambda item: item['ticker_id'],reverse=True)

    tmp={'tickerdatalist':tickerdatalist}

    return render(request, 'active.html',tmp)

def pending(request):
    return render(request, 'pending.html')   

@login_required
def history(request):
    return render(request, 'history.html') 

@login_required
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
        
@login_required
def schedule(request,id):

    if request.method == 'POST':
        
        a=request.POST.get('wingselection')
        b=request.POST.get('floorselection')
        c=request.POST.get('roomselection')

        if (request.POST.get('scheduleenabler')!=None):
            print('Inside enabler')
        else:
            print('Outside enabler')
        
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')

        created_for=str(a)+' '+str(b)+' '+str(c)
        
        t=TickerDetails.objects.filter(ticker_id=int(id)).values()

        t.update(ticker_start_time=start_date,ticker_end_time=end_date,created_for=created_for)

        return redirect('/')

    else:
        roomconfig=filterData('resources/resourcexml')
        roomconfig['ticker_id']=id
        frequency = [
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
            ]

        days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

        roomconfig['routine']=frequency
        roomconfig['routine_days']=days

        return render(request, 'schedule.html',roomconfig)

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



@api_view(['GET', 'POST', 'DELETE'])
def taskPost(request,pk="0"):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            print("valid")
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'GET':
        tasks = Task.objects.all().order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        serializer = TaskSerializer(data=request.data)
        p=serializer.initial_data
        q=int(p.get('id'))
        print(type(q))
        task = Task.objects.get(id=q)
        task.delete()

        return Response('Item succsesfully delete!')