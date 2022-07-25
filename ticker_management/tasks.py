from celery import shared_task
from .models import TickerDetails
from datetime import datetime
import json
import subprocess
from ticker_management.rundecklog import initial_data

@shared_task(bind=True)
def makeMeAlive(self):
    print("Make System Alive")

@shared_task(bind=True)
def callticker(self,command,ticker_id):
    try:    
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
        process_output=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # rundeck_id=0
        (output, err) = process_output.communicate()

        # p_status = output.wait()
        # print("Command output : ", output.decode())
        # print("Command exit status/return code : ", p_status)


        rundeck_obj=json.loads(output.decode())
        rundeckid=int(rundeck_obj.get('id'))
        deleted=False
        now = datetime.now()
        
        if (ticker_obj.get().get('frequency')=='1'):
            deleted=True
        
        if deleted:
            ticker_obj.deleted_on = now.strftime("%Y-%m-%d %H:%M:%S")
            ticker_obj.update(rundeckid=rundeckid,is_deleted=1,is_active=0) 
        else:
            if ticker_obj.get().get('ticker_end_time')<=now:
                ticker_obj.deleted_on = now.strftime("%Y-%m-%d %H:%M:%S")
                ticker_obj.update(rundeckid=rundeckid,is_deleted=1,is_active=0)
            else:
                ticker_obj.update(rundeckid=rundeckid)
        
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
        initial_data(ticker_obj)
    except TickerDetails.DoesNotExist as e:
        print('No such id found :',e)

# @shared_task(bind=True)
# def celery_beat_name(self):
#     command = ['sshpass -p 1 ssh -p7010 -X -o StrictHostKeyChecking=no guest@172.22.12.62 ticker-birthday']
#     subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
