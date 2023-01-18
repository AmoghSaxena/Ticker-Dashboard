import json
import xml.etree.ElementTree as ET
from ticker_dashboard.settings import BASE_DIR
from ticker_management.models import TickerDetails
from datetime import timedelta,datetime
from django.db.models import Q

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
    if newTickerRoomList=='All':
        return True
    for i in newTickerRoomList:
        if i in runningTickerRoomList:
            return True
    return False

def findRoomNumber(wings,floors,rooms):
    idList = list()
    filePath=f"{str(BASE_DIR)}/static/resources/"

    file=open(filePath+"resource.json")

    datafromdvs=json.load(file)

    tree = ET.parse(filePath+"resource.xml")
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

def checkPriority(newTickerPriority,wings,floors,rooms,startTime,endTime,timeInterval):

    if endTime is not None:
        ticker_list=TickerDetails.objects.all().filter(Q(ticker_start_time__range=(startTime,endTime)) |
                                                            Q(ticker_end_time__range=(startTime,endTime))).values()
    else:
        endTime=datetime.strptime(startTime,"%Y-%m-%dT%H:%M")+timedelta(minutes=int(timeInterval))

        ticker_list=TickerDetails.objects.all().filter(Q(ticker_start_time__range=(startTime,endTime)) |
                                                            Q(ticker_end_time__range=(startTime,endTime))).values()
    
    runningTicker=dict()
    
    if len(ticker_list)>0:
        wings=wings
        floors=floors
        rooms=rooms

        roomList=findRoomNumber(wings,floors,rooms)

        priority=['Low','Medium','High','Emergency']

        for ticker in ticker_list:
            if ticker['ticker_priority']!='Emergency':
                if ticker['rooms']=='All':
                    runningTicker['runningTickerObj']=ticker
                    break
                else:
                    rooms_str=ticker['rooms'].strip('[]')
                    rooms=list()
                    strToList(rooms,rooms_str)

                    if commonRooms(roomList['rooms'],rooms):
                        runningTicker['runningTicker']=ticker
                        break
            else:
                runningTicker['runningTicker']=ticker
                break

        if len(runningTicker)>0:
            a=priority.index(runningTicker['runningTicker']['ticker_priority'])
            b=priority.index(newTickerPriority)

            if b>a:
                runningTicker['message']="New ticker has higher priority than running ticker.\nDO YOU REALLY WANT TO OVERRIDE?"
            else:
                runningTicker['message']="New ticker has lower priority than running ticker.\nDO YOU REALLY WANT TO OVERRIDE?"
            return {'status':True,'runningTicker':runningTicker}
        else:
            runningTicker['message']="Are you sure, You want to create ticker?"
            return {'status':False,'runningTicker':runningTicker}

    else:
        runningTicker['message']="Are you sure, You want to create ticker?"
        return {'status':False,'runningTicker':runningTicker}



    # wings=request.POST.getlist('wingSelection')
    # floors=request.POST.getlist('floorSelection')
    # rooms=request.POST.getlist('roomSelection')

    # roomList=findRoomNumber(wings,floors,rooms)

    # priority=['Low','Medium','High','Emergency']

    # runningTicker=dict()

    # for ticker in tickerDetailsDB:
    #     if ticker['ticker_priority']!='Emergency':
    #         if ticker['rooms']=='All':
    #             runningTicker['runningTickerObj']=ticker
    #             break
    #         else:
    #             rooms_str=ticker['rooms'].strip('[]')
    #             rooms=list()
    #             strToList(rooms,rooms_str)

    #             if commonRooms(roomList['rooms'],rooms):
    #                 runningTicker['runningTicker']=ticker
    #                 break
    # if len(runningTicker)>0:
    #     a=priority.index(runningTicker['runningTicker']['ticker_priority'])
    #     b=priority.index(newTickerPriority)

    #     if b>a:
    #         runningTicker['message']="New ticker has higher priority than running ticker.\nDO YOU REALLY WANT TO OVERRIDE?"
    #     else:
    #         runningTicker['message']="New ticker has lower priority than running ticker.\nDO YOU REALLY WANT TO OVERRIDE?"
    #     return runningTicker

def roomConfigurations(ticker_obj):
    logger.info('Inside roomConfiguration function')
    
    # ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
    
    wings_str=ticker_obj.get()['wings'].strip('[]')
    floors_str=ticker_obj.get()['floors'].strip('[]')
    rooms_str=ticker_obj.get()['rooms'].strip('[]')

    print(wings_str,floors_str,rooms_str)

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

def removeDuplicate(listObj,stringObj):
    stringObj=stringObj.replace("[","").replace("]","")

    data=str()

    for i in stringObj:
        if i==',':
            data=data.replace("{","").replace("}","")
            if data.split(":")[0].replace("'",'') not in listObj[0].keys():
                listObj.append({data.split(":")[0].replace("'",''): data.split(":")[1].strip()})
            data=str()
        else:
            data+=i
    
    if len(data)>0:
        data=data.replace("{","").replace("}","")
        if data.split(":")[0].replace("'",'') not in listObj[0].keys():
            listObj.append({data.split(":")[0].replace("'",''): data.split(":")[1].strip()})