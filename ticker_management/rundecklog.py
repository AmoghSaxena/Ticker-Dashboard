from .models import SetUp, RundeckLog
import requests

#Loggers
import logging
logger=logging.getLogger('dashboardLogs')

def initial_data(ticker_obj,basicTickerInfo):
    logger.info('Inside initial_data function')
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
            RundeckLog_obj.ticker_title=ticker_obj.get()['ticker_title']
            RundeckLog_obj.execution=status
            RundeckLog_obj.successfull_nodes=successfulNodes
            RundeckLog_obj.failed_nodes=failedNodes
            RundeckLog_obj.save()
            if status == 'succeeded' or status == 'aborted' or status == 'failed':
                errorLog = requests.get(f"https://{basicTickerInfo['FQDN']}/r/api/{basicTickerInfo['Rundeck_Api_Version']}/execution/{basicTickerInfo['rundeckid']}/output/", headers={"X-Rundeck-Auth-Token": basicTickerInfo['Rundeck_Token'], "Content-Type":"application/json", "Accept": "application/json"})
                errorLogOutput = errorLog.json()
                errorLog = errorLogOutput['entries'][-1]['log']
                return errorLog
        else:
            logger.warning('Response status code is not 200')
        return 'Success'
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
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')

            RundeckLog.objects.filter(rundeck_id=rundeckid).update(execution=status,successfull_nodes=successfulNodes,failed_nodes=failedNodes)

            if status == 'succeeded' or status == 'aborted' or status == 'failed':
                errorLog = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/output/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
                errorLogOutput = errorLog.json()
                errorLog = errorLogOutput['entries'][-1]['log']
                return errorLog
        else:
            logger.warning('Response status code is not 200')
    except Exception as e:
        logger.error(e)

def abortTicker(ticker_obj):
    logger.info('Inside abortTicker function')
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
                errorLog = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/output/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
                errorLogOutput = errorLog.json()
                errorLog = errorLogOutput['entries'][-1]['log']
                if status == 'aborted':
                    requests.post(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/job/{Rundeck_Stop_Job}/run/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"}, json={ "argString": f"-whichnode \"{nodes}\""})
                return errorLog
            elif status == 'running':
                requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/abort/", headers={"X-Rundeck-Auth-Token": Rundeck_Token})
        else:
            logger.warning('Response status code is not 200')
    except Exception as e:
        logger.error(e)