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
def callticker(self,json_data,ticker_id):
    logger.info('Inside callticker function')
    try:
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()

        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get()['FQDN']
        Rundeck_Token=setupData.get()['Rundeck_Token']
        Rundeck_Start_Job=setupData.get()['Rundeck_Start_Job']
        Rundeck_Stop_Job=setupData.get()['Rundeck_Stop_Job']
        Rundeck_Api_Version=setupData.get()['Rundeck_Api_Version']

        headers = {
            'Accept': 'application/json',
            'X-Rundeck-Auth-Token': Rundeck_Token
        }

        response = requests.post(f'https://{FQDN}/r/api/17/job/{Rundeck_Start_Job}/run', headers=headers, json=json_data)
        
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
        
        ticker_obj=TickerDetails.objects.filter(ticker_id=ticker_id).values()
        initial_data(ticker_obj)
        print('After initial')
    except TickerDetails.DoesNotExist as e:
        logger.error(f"{ticker_id} doesn't exists")
