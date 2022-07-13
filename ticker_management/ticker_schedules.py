import subprocess
import json
import xml.etree.ElementTree as ET
from .models import SetUp
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def xmlFileRead(tagList,idList,root):
    
    for id in idList:

        for child in root:
            if child.get('key_id') and child.get('key_id') == str(id):
                tagList.append(child.get('name'))
    st=str()
    for i in tagList:
        st+=str(i)+' '

    # print(st)

    return st.strip()

def roomConfigurations(request):

    wings=request.POST.getlist('wingSelection')
    floors=request.POST.getlist('floorSelection')
    rooms=request.POST.getlist('roomSelection')

    print(wings,type(wings))
    print(floors,type(floors))
    print(rooms,type(rooms))

    idList = list()

    file=open(f"{BASE_DIR}/resources/resource.json")

    datafromdvs=json.load(file)


    tree = ET.parse(f"{BASE_DIR}/resources/res.xml")
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


def schedule_tasks():
    pass

def schedulingticker(request,ticker_id):

    setup=SetUp.objects.filter(id=1).values()

    FQDN=setup.get().get('FQDN')
    Dvs_Token=setup.get().get('Dvs_Token')
    Rundeck_Token=setup.get().get('Rundeck_Token')
    Apache_server_url=setup.get().get('Apache_server_url')
    Ticker_FQDN=setup.get().get('Ticker_FQDN')

    command=str()
    part_a=str()
    part_b=str()

    print("inside 1")

    configuration=roomConfigurations(request)
    
    print("inside 2")

    part_a="curl --location --request POST 'https://"+str(FQDN)+"/r/api/17/job/0d0c3cfe-adcd-4f86-8c03-adaa1cd2c0e0/run' --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'X-Rundeck-Auth-Token: "+str(Rundeck_Token)+"""' --header 'Cookie: JSESSIONID=56pr1s6s16yt1fsckqzcyjwfc' --data-raw '{ "argString": "-whichnode \\"""+'"'+str(configuration)+'''\\" -FQDN \\'''
    part_b='"'+str(Ticker_FQDN)+'\\" -jsonFile \\"'+str(ticker_id)+"""\\" -BasicAuth \\"YWRtaW46YWRtaW4xMjM0\\""}'"""
    
    command=part_a+part_b
    if (len(command)>0):

        print("inside 0")

        if request.POST.get('tickerSelecter')== 'emergency' or request.POST.get('scheduleEnabler') == 'enabled':

            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        else:

            schedule_tasks(configuration,ticker_id,request)

    else:
        print("No scheduled processes")



"""
            ALL USED APIs

1.  curl --location --request POST 'https://dvs-uatblue.digivalet.com/r/api/17/job/0d0c3cfe-adcd-4f86-8c03-adaa1cd2c0e0/run' --header 'Accept: 
    application/json' --header 'X-Rundeck-Auth-Token: GPE0a5rF328fUHV9Zwj1kmQSudVY0zOn' --header 'Content-Type: application/json' --data-raw '
    { "argString": "-whichnode \"standard-1274\" -FQDN \"ticker.dns.army\" -jsonFile \"48\""}'

2.  curl --location --request POST 'https://dvs-uatblue.digivalet.com/r/api/17/job/0d0c3cfe-adcd-4f86-8c03-adaa1cd2c0e0/run' --header 'Content-Type: 
    application/json' --header 'Accept: application/json' --header 'X-Rundeck-Auth-Token: GPE0a5rF328fUHV9Zwj1kmQSudVY0zOn' --header 'Cookie: JSESSIONID=
    c7ttfr9ur2t4giiq0voyyz7q' --data-raw '{ "argString": "-whichnode \"tags: '\''Standard'\''\" -FQDN \"ticker.dns.army\" -jsonFile \"64\" -BasicAuth 
    \"YWRtaW46YWRtaW4xMjM0\"" 

3.  curl --location --request POST 'https://dvs-uatblue.digivalet.com/r/api/17/job/0d0c3cfe-adcd-4f86-8c03-adaa1cd2c0e0/run' \
    --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    --header 'X-Rundeck-Auth-Token: GPE0a5rF328fUHV9Zwj1kmQSudVY0zOn' \
    --header 'Cookie: JSESSIONID=56pr1s6s16yt1fsckqzcyjwfc' \
    --data-raw '{
    "argString": "-whichnode \"standard-1274\" -FQDN \"ticker.dns.army\" -jsonFile \"64\" -BasicAuth \"YWRtaW46YWRtaW4xMjM0\""

4.  

"""