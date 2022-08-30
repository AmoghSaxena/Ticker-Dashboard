from celery import shared_task
from .models import TickerDetails,SetUp
from datetime import datetime
import json
import requests
from ticker_management.rundecklog import initial_data

#Loggers
import logging
logger=logging.getLogger('dashboardLogs')

@shared_task(bind=True)
def callticker(self,basicTickerInfo,ticker_obj):
    logger.info('Inside callticker function')
    try:

        if int(ticker_obj.get()['is_deleted'])==0:

            headers = {
                'Accept': 'application/json',
                'X-Rundeck-Auth-Token': basicTickerInfo['Rundeck_Token']
            }
            # response = requests.post(f'https://{basicTickerInfo['FQDN']}/r/api/17/job/{Rundeck_Start_Job}/run', headers=headers, json=json_data)
            response = requests.post(f'https://{basicTickerInfo["FQDN"]}/r/api/{basicTickerInfo["Rundeck_Api_Version"]}/job/{basicTickerInfo["Rundeck_Start_Job"]}/run', headers=headers, json=basicTickerInfo["json_data"])
        
            rundeck_obj=response.json()
            rundeckid=int(rundeck_obj['id'])
            deleted=False
            now = datetime.now()
            
            if (ticker_obj.get()['frequency']=='1'):
                deleted=True
            
            if deleted:
                ticker_obj.update(rundeckid=rundeckid,is_deleted=1,is_active=0,deleted_on=now.strftime("%Y-%m-%d %H:%M:%S")) 
            else:
                if ticker_obj.get()['ticker_end_time']<=now:
                    ticker_obj.update(rundeckid=rundeckid,is_deleted=1,is_active=0,deleted_on=now.strftime("%Y-%m-%d %H:%M:%S")) 
                else:
                    ticker_obj.update(rundeckid=rundeckid)
            
            basicTickerInfo.pop('json_data')

    except Exception as e:
        logger.error(f"Error while execution of task: {e}")

    initial_data(ticker_obj,basicTickerInfo)
    print('After initial')
