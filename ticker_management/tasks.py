from celery import shared_task
from .models import TickerDetails
from datetime import datetime
import json
import subprocess
from ticker_management.rundecklog import initial_data

#Loggers
import logging
logger=logging.getLogger('dashboardLogs')

@shared_task(bind=True)
def callticker(self,command,ticker_id):
    try:
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
        process_output=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, err) = process_output.communicate()

        rundeck_obj=json.loads(output.decode())
        rundeckid=int(rundeck_obj.get('id'))
        deleted=False
        now = datetime.now()
        
        if (ticker_obj.get().get('frequency')=='1'):
            deleted=True
        
        if deleted:
            ticker_obj.update(rundeckid=rundeckid,is_deleted=1,is_active=0,deleted_on=now.strftime("%Y-%m-%d %H:%M:%S")) 
        else:
            if ticker_obj.get().get('ticker_end_time')<=now:
                ticker_obj.update(rundeckid=rundeckid,is_deleted=1,is_active=0,deleted_on=now.strftime("%Y-%m-%d %H:%M:%S")) 
            else:
                ticker_obj.update(rundeckid=rundeckid)
        
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
        initial_data(ticker_obj)
    except TickerDetails.DoesNotExist as e:
        logger.error(f"{ticker_id} doesn't exists")
