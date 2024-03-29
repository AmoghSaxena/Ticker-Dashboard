from .models import SetUp, RundeckLog
import requests
from datetime import datetime,timedelta

from threading import Thread
from .models import TickerDetails

#Loggers
import logging
logger=logging.getLogger('dashboardLogs')

def initial_data(ticker_obj,basicTickerInfo):
    logger.info('Creating rundeck data in DB')
    try:
        rundeckid=ticker_obj.get()['rundeckid']
        
        response = requests.get(f"https://{basicTickerInfo['FQDN']}/r/api/{basicTickerInfo['Rundeck_Api_Version']}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": basicTickerInfo['Rundeck_Token'], "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
        if response.status_code == 200:
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')
                
            RundeckLog_obj=RundeckLog()
            RundeckLog_obj.rundeck_id=rundeckid
            RundeckLog_obj.ticker_id=ticker_obj.get()['ticker_id']
            RundeckLog_obj.time_interval=datetime.now()+timedelta(seconds=basicTickerInfo['time_interval'])
            RundeckLog_obj.ticker_title=ticker_obj.get()['ticker_title']
            RundeckLog_obj.execution=status
            RundeckLog_obj.tickerStatus='running'
            RundeckLog_obj.successfull_nodes=successfulNodes
            RundeckLog_obj.failed_nodes=failedNodes
            RundeckLog_obj.save()
        else:
            logger.error('Response status code is not 200')
    except Exception as e:
        logger.error(e)

def rundeck_update(rundeckid):
    try:
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get()['FQDN']
        Rundeck_Token=setupData.get()['Rundeck_Token']
        Rundeck_Stop_Job=setupData.get()['Rundeck_Stop_Job']
        Rundeck_Api_Version=setupData.get()['Rundeck_Api_Version']
        
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
        if response.status_code == 200:

            rundeckLog=RundeckLog.objects.filter(rundeck_id=rundeckid).values()

            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')

            if (status=='failed' or status=='aborted'):
                if len(successfulNodes)>0:
                    if datetime.now()>=rundeckLog.get()['time_interval']:
                        rundeckLog.update(execution=status,successfull_nodes=successfulNodes,failed_nodes=failedNodes,tickerStatus='succeeded')
                    else:
                        rundeckLog.update(execution=status,successfull_nodes=successfulNodes,failed_nodes=failedNodes,tickerStatus='running')    
                else:
                    rundeckLog.update(execution=status,successfull_nodes=successfulNodes,failed_nodes=failedNodes,tickerStatus=status)
            elif datetime.now()>=rundeckLog.get()['time_interval']:
                rundeckLog.update(execution=status,successfull_nodes=successfulNodes,failed_nodes=failedNodes,tickerStatus='succeeded')
            else:
                rundeckLog.update(execution=status,successfull_nodes=successfulNodes,failed_nodes=failedNodes)
        else:
            logger.error('Response status code is not 200')
    except Exception as e:
        logger.error(e)

def abortTicker(ticker_obj):
    logger.info('Aborting ticker from UI')
    try:
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get()['FQDN']
        Rundeck_Token=setupData.get()['Rundeck_Token']
        Rundeck_Stop_Job=setupData.get()['Rundeck_Stop_Job']
        Rundeck_Api_Version=setupData.get()['Rundeck_Api_Version']

        rundeckid=ticker_obj.get()['rundeckid']
        
        rundeckid=ticker_obj.get()['rundeckid']
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
        if response.status_code == 200:
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')
            RundeckLog_obj=RundeckLog()
            RundeckLog_obj.rundeck_id=rundeckid
            RundeckLog_obj.ticker_id=ticker_obj.get()['ticker_id']
            RundeckLog_obj.ticker_title=ticker_obj.get()['ticker_title']
            RundeckLog_obj.execution=status
            RundeckLog_obj.successfull_nodes=successfulNodes
            RundeckLog_obj.failed_nodes=failedNodes
            RundeckLog_obj.save()
            nodes = ''
            if len(successfulNodes) < 1:
                successfulNodes.append(" ")
            if len(failedNodes) < 1:
                failedNodes.append(" ")
            nodes = ' '.join(successfulNodes) + ' ' + ' '.join(failedNodes)
            if status == 'succeeded' or status == 'aborted' or status == 'failed':
                pass
                # errorLog = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/output/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
                # errorLogOutput = errorLog.json()
                # errorLog = errorLogOutput['entries'][-1]['log']
                # if status == 'aborted':
                #     requests.post(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/job/{Rundeck_Stop_Job}/run/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"}, json={ "argString": f"-whichnode \"{nodes}\""})
                # return errorLog
            elif status == 'running':
                requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/abort/", headers={"X-Rundeck-Auth-Token": Rundeck_Token})
        else:
            logger.error('Response status code is not 200')
    except Exception as e:
        logger.error(e)

def killTicker(ticker_obj):
    try:
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get()['FQDN']
        Rundeck_Token=setupData.get()['Rundeck_Token']
        Rundeck_Stop_Job=setupData.get()['Rundeck_Stop_Job']
        Rundeck_Api_Version=setupData.get()['Rundeck_Api_Version']
        
        rundeckid=ticker_obj.get()['rundeckid']
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
       
        if response.status_code == 200:
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')

            RundeckLog_obj=RundeckLog.objects.filter(rundeck_id=rundeckid).values()

            RundeckLog_obj.update(execution=status,tickerStatus='aborted',successfull_nodes=successfulNodes,failed_nodes=failedNodes)

            nodes = ''
            if len(successfulNodes) < 1:
                successfulNodes.append(" ")

            if len(failedNodes) < 1:
                failedNodes.append(" ")

            nodes = ' '.join(successfulNodes) + ' ' + ' '.join(failedNodes)


            requests.post(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/job/{Rundeck_Stop_Job}/run/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"}, json={ "argString": f"-whichnode \"{nodes}\""})
            logger.info('Kill Ticker from UI')
        else:
            logger.error('Response status code is not 200')

    except Exception as e:
        logger.error(e)

def killTickerForPriority(ticker_obj,nodes):
    try:
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get()['FQDN']
        Rundeck_Token=setupData.get()['Rundeck_Token']
        Rundeck_Stop_Job=setupData.get()['Rundeck_Stop_Job']
        Rundeck_Api_Version=setupData.get()['Rundeck_Api_Version']
        
        rundeckid=ticker_obj.get()['rundeckid']
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
       
        if response.status_code == 200:
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')

            RundeckLog_obj=RundeckLog.objects.filter(rundeck_id=rundeckid).values()

            RundeckLog_obj.update(execution=status,tickerStatus='aborted',successfull_nodes=successfulNodes,failed_nodes=failedNodes)

            requests.post(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/job/{Rundeck_Stop_Job}/run/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"}, json={ "argString": f"-whichnode \"{nodes}\""})
        else:
            logger.error('Response status code is not 200')

    except Exception as e:
        logger.error(e)

def abortForPriority(id,nodes):
    try:
        ticker_obj=TickerDetails.objects.filter(ticker_id=int(id)).values()
        
        if ticker_obj.get()['rundeckid']!=None:
            killTickerForPriority(ticker_obj,nodes)
            rundeckLogData=RundeckLog.objects.all().filter(ticker_id=int(id)).values()
            rundeckLog=sorted(rundeckLogData,key=lambda item: item['rundeck_id'],reverse=True)
        
        TickerDetails.objects.filter(ticker_id=int(id),frequency='1').values().update(ticker_end_time=datetime.now())
        logger.info('Successfully aborted ticker when priority calls')
    except Exception as err:
        logger.error(err)