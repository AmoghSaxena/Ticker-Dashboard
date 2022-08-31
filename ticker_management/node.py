import json
import xml.etree.ElementTree as ET
from ticker_dashboard.settings import BASE_DIR
from ticker_management.models import TickerDetails
from datetime import datetime

import logging
logger=logging.getLogger('dashboardLogs')

priority=['Low','Medium','High','Emergency']

def xmlFileRead(tagList,idList,root):
    for id in idList:
        for child in root:
            if child.get('key_id') and child.get('key_id') == str(id):
                if child.get('name') not in tagList:
                    tagList.append(child.get('name'))

def strToList(listConfig,stringConfig):
    if "'" in stringConfig:
        data=str()
        count=False
        for i in stringConfig:
            if i!=',':
                if i=="'":
                    if count:
                        if len(data)>0:
                            listConfig.append(data)
                            data=str()
                        count=False
                    else:
                        count=True
                else:
                    if count:
                        data+=i

def getTickerId(tickerDetailsDB,ip):
    
    tree = ET.parse(f"{str(BASE_DIR)}/static/resources/resource.xml")
    root = tree.getroot()

    key_name=str()

    for child in root:
        if child.get('ip') and child.get('ip') == str(ip):
            key_name=child.get('name')
            break

    if len(key_name)>0:
        for ticker in tickerDetailsDB:
            if str(key_name) in ticker['rooms']:
                return {"key_name":key_name,"ticker_id":ticker['ticker_id']}
            elif ticker['wings']=='All' and ticker['floors']=='All' and ticker['rooms']=='All':
                return {"key_name":key_name,"ticker_id":ticker['ticker_id']}
        
        return {"key_name":key_name,"ticker_id":-1}
    else:
        return {"key_name":"Not Found","ticker_id":-1}

def commonRooms(runningTickerRoomList,newTickerRoomList):
    for i in runningTickerRoomList:
        if i in newTickerRoomList:
            return True
    return False

def findRoomNumber(wings,floors,rooms):
    idList = list()

    file=open(f"{str(BASE_DIR)}/static/resources/resource.json")

    datafromdvs=json.load(file)

    tree = ET.parse(f"{str(BASE_DIR)}/static/resources/resource.xml")
    root = tree.getroot()

    roomList=list()

    if (len(rooms)==0) or rooms[0]=='All':
        if (len(floors)==0 or floors[0]=='All'):
            if (len(wings)==0 or wings[0]=='All'):
                return {'wings':'All','floors':'All','rooms':'All'}
                # return '.*'
                # return roomList
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
        else:
            for parFloor in floors:
                for items in datafromdvs.get('data'):
                    if items.get('floor_name')!=None and items.get('floor_name') == parFloor:
                        idList.append(items.get('id'))
    else:
        for parRoom in rooms:
            for items in datafromdvs.get('data'):
                if items.get('key_number')!=None and items.get('key_number') == parRoom:
                    idList.append(items.get('id'))
    
    xmlFileRead(roomList,idList,root)

    return {'wings':'[]','floors':'[]','rooms':roomList}

def checkPriority(request):
    wings=request.POST.getlist('wingSelection')
    floors=request.POST.getlist('floorSelection')
    rooms=request.POST.getlist('roomSelection')

    roomList=findRoomNumber(wings,floors,rooms)

    priority=['Low','Medium','High','Emergency']

    tickerSelection=request.POST.get('tickerSelecter')

    if tickerSelection == 'scrolling':
        newTickerPriority=request.POST.get('scrollingTickerPriority')
    elif tickerSelection == 'media':
        newTickerPriority=request.POST.get('mediaTickerPriority')
    elif tickerSelection == 'emergency':
        newTickerPriority="Emergency"

    tickerDetailsDB = TickerDetails.objects.all().filter(ticker_start_time__lte=datetime.now(),ticker_end_time__gt=datetime.now())
    
    runningTicker=dict()

    for ticker in tickerDetailsDB:
        if ticker['ticker_priority']!='Emergency':
            if ticker['rooms']=='All':
                runningTicker['runningTickerObj']=ticker
                break
            else:
                rooms_str=ticker.get()['rooms'].strip('[]')
                rooms=list()
                strToList(rooms,rooms_str)

                if commonRooms(roomList,rooms):
                    runningTicker=ticker
                    break
    if len(runningTicker)>0:
        a=priority.index(runningTicker['ticker_priority'])
        b=priority.index(newTickerPriority)

        if b>a:
            runningTicker['message']="New ticker has higher priority than running ticker.\nDO YOU REALLY WANT TO OVERRIDE?"
        else:
            runningTicker['message']="New ticker has lower priority than running ticker.\nDO YOU REALLY WANT TO OVERRIDE?"
        return runningTicker

def roomConfigurations(ticker_obj):
    logger.info('Inside roomConfiguration function')
    
    # ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
    
    wings_str=ticker_obj.get()['wings'].strip('[]')
    floors_str=ticker_obj.get()['floors'].strip('[]')
    rooms_str=ticker_obj.get()['rooms'].strip('[]')

    wings=list()
    floors=list()
    rooms=list()

    strToList(wings,wings_str)
    strToList(floors,floors_str)
    strToList(rooms,rooms_str)

    print(wings)
    print(floors)
    print(rooms)

    data=findRoomNumber(wings,floors,rooms)

    return data
