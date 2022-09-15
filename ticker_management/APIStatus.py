""" Response Output """
res = {
    "status": None,
    "statusCode": None,
    "message": None
}

resp = {
    "status": None,
    "statusCode": None,
    "message": None,
    "data": None
}


""" Reboot Status Case """    #### STATUS 6XX #### 
rebootSuccessStatus = {"message": "Ticker Re-Scheduled", "statusCode": 601}
rebootFailureStatus = {"message": "Ticker Time Out", "statusCode": 602}
rebootNodeNotFound = {"message": "Node Not Found", "statusCode": 603}
rebootNotReschedule = {"message": "Error In Ticker Re-Schedule", "statusCode": 604}
rebootStatusError = {"message": "Error Occurred During Ticker Re-Scheduled", "statusCode": 605}


""" TV ipad Status Case """    #### STATUS 7XX #### 
tvIpadSuccessStatus = {"message": "Status Updated", "statusCode": 701}
tickerNotFound = {"message": "Ticker Not Found", "statusCode": 702}
dataNotFound = {"message": "Required Data Not Found", "statusCode": 703}
dvcNotFound = {"message": "Controller Not Found", "statusCode": 704}
tvIpadStatusError = {"message": "Error Occurred During Update Status", "statusCode": 705}


""" Ticker Close Case """    #### STATUS 8XX #### 
tickerCloseStatus = {"message": "Data Updated", "statusCode": 801}
TickerCloseError = {"message": "Error Occurred During ", "statusCode": 805}


""" Validation Case """    #### STATUS 9XX ####
validationError = {"message": "Error Occurred During Token verify", "statusCode": 901}


""" Request Verify Case """    #### STATUS 12XX ####
requestInvalid = {"message": "Invalid Request", "statusCode": 1201}
requestBody = {"message": "Data Not Exists at Body", "statusCode": 1202}


""" header data Case """    #### STATUS 13XX ####
tokenPresent = {"message": "Token Not Found", "statusCode": 1301}
ipAddressPresent = {"message": "IP Address Not Found", "statusCode": 1302}


""" Verify Case"""    #### STATUS 14XX ####
tokenFailure = {"message": "Invalid Token", "statusCode": 1401}
ipAddressFailure = {"message": "Invalid IP Address", "statusCode": 1402}


""" Databases Error """   #### STATUS 15XX ####
DBError = {"message": "DB Error", "statusCode": 1501}


""" Config API Case """   #### STATUS 16XX ####
ConfigNotFoundFailure = {"message": "Ticker Not Exists", "statusCode": 1601}
ConfigFailure = {"message": "Error Occurred During Fetched Config File", "statusCode": 1602}


""" DND Status API Case """   #### STATUS 17XX ####
dndStatusSuccess = {"message": "Status Update", "statusCode": 1701}
b = {"message": "Ticker Not Exists", "statusCode": 1702}
dndStatusError = {"message": "Error Occurred During Update Status", "statusCode": 1703}



""" Close Ticker API Case """   #### STATUS 18XX ####
closeTickerAPISuccess = {"message": "Ticker Close Successfully", "statusCode": 1801}
closeTickerAPIFailure = {"message": "Error Occurred During Close Ticker", "statusCode": 1802}


""" Priority Ticker API Case """   #### STATUS 18XX ####
priorityTickerAPISuccess = {"message": "Ticker Priority Check Successfully", "statusCode": 1901}
priorityTickerAPIFailure = {"message": "Error Occurred During Check Priority Ticker", "statusCode": 1902}