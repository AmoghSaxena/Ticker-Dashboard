from cmath import e
from .models import SetUp, RundeckLog
import requests,json

def initial_data(ticker_obj):
    try:
        rundeckid=ticker_obj.get().get('rundeckid')
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get().get('FQDN')
        Rundeck_Token=setupData.get().get('Rundeck_Token')
        Rundeck_Api_Version=setupData.get().get('Rundeck_Api_Version')
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
        if response.status_code == 200:
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')
            RundeckLog_obj=RundeckLog()
            RundeckLog_obj.rundeck_id=rundeckid
            RundeckLog_obj.ticker_id=ticker_obj.get().get('ticker_id')
            RundeckLog_obj.ticker_title=ticker_obj.get().get('ticker_title')
            RundeckLog_obj.execution=status
            RundeckLog_obj.successfull_nodes=successfulNodes
            RundeckLog_obj.failed_nodes=failedNodes
            RundeckLog_obj.save()
            if status == 'succeeded' or status == 'aborted' or status == 'failed':
                errorLog = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/output/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
                errorLogOutput = errorLog.json()
                errorLog = errorLogOutput['entries'][-1]['log']
            return errorLog
        else:
            print("Response status code is not 200")
    except Exception as e:
        print(e)


def abortTicker(ticker_obj):
    try:
        rundeckid=ticker_obj.get().get('rundeckid')
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get().get('FQDN')
        Rundeck_Token=setupData.get().get('Rundeck_Token')
        Rundeck_Stop_Job=setupData.get().get('Rundeck_Stop_Job')
        Rundeck_Api_Version=setupData.get().get('Rundeck_Api_Version')
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token, "Content-Type":"application/json", "Accept": "application/json"})
        rundeckOutput = response.json()
        if response.status_code == 200:
            status = rundeckOutput['status']
            successfulNodes = rundeckOutput.get('successfulNodes','[]')
            failedNodes = rundeckOutput.get('failedNodes', '[]')
            RundeckLog_obj=RundeckLog()
            RundeckLog_obj.rundeck_id=rundeckid
            RundeckLog_obj.ticker_id=ticker_obj.get().get('ticker_id')
            RundeckLog_obj.ticker_title=ticker_obj.get().get('ticker_title')
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
            elif status == 'running':
                requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/abort/", headers={"X-Rundeck-Auth-Token": Rundeck_Token})
            return errorLog
        else:
            print("Response status code is not 200")
    except Exception as e:
        print(e)