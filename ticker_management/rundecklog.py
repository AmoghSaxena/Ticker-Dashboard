from .models import SetUp,RundeckLog
import requests
import xml.etree.ElementTree

def initial_data(ticker_obj):
    try:
        rundeckid=ticker_obj.get().get('rundeckid')
        setupData=SetUp.objects.filter(id=1).values()
        FQDN=setupData.get().get('FQDN')
        Rundeck_Token=setupData.get().get('Rundeck_Token')
        Rundeck_Api_Version=setupData.get().get('Rundeck_Api_Version')
        response = requests.get(f"https://{FQDN}/r/api/{Rundeck_Api_Version}/execution/{rundeckid}/", headers={"X-Rundeck-Auth-Token": Rundeck_Token})
        if response.status_code == 200:
            xmlDocument = xml.etree.ElementTree.fromstring(response.text)
            status = xmlDocument.find("./execution").get('status')
            successfulNodes = [node.get('name') for node in xmlDocument.findall("./execution/successfulNodes/node")]
            failedNodes = [node.get('name') for node in xmlDocument.findall("./execution/failedNodes/node")]
            RundeckLog_obj=RundeckLog()
            RundeckLog_obj.rundeck_id=rundeckid
            RundeckLog_obj.ticker_id=ticker_obj.get().get('ticker_id')
            RundeckLog_obj.ticker_title=ticker_obj.get().get('ticker_title')
            RundeckLog_obj.execution=status
            RundeckLog_obj.successfull_nodes=successfulNodes
            RundeckLog_obj.failed_nodes=failedNodes
            RundeckLog_obj.save()
        else:
            print("Response status code is not 200")
    except Exception as e:
        print(e)