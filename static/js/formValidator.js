

function notification() {

    var modal = document.getElementById("notificationModal");
    var span = document.getElementsByClassName("close")[0];

    modal.style.display = "block";

    span.onclick = function() {
        modal.style.display = "none";
    }

    var select = document.getElementById("tickerSelecter");
    var option = select.options[select.selectedIndex];

    var priority,timeInterval;

    if (option.text == "Scrolling Ticker")
    {
        priority=document.getElementById("scrollingTickerPriority").value;
        timeInterval=document.getElementById("scrollingTickerTimeInterval").value;
    }
    else if (option.text == "Media Ticker")
    {
        priority=document.getElementById("mediaTickerPriority").value;
        timeInterval=document.getElementById("mediaTickerTimeInterval").value;
    }
    else
    {
        priority="Emergency";
    }

    if (document.getElementById("scheduleEnabler").checked)
    {
        var nowTime= new Date();
        startTime=nowTime.getFullYear()+"-"+(nowTime.getMonth()+1)+"-"+nowTime.getDate()+"T"+nowTime.getHours()+":"+nowTime.getMinutes();
        endTime=null;
        if (priority=="Emergency")
        {
            timeInterval="864000";
        }
    }
    else
    {
        if (document.getElementById("onetime").checked)
        {
            startTime=document.getElementById("startDate").value;
            endTime=null;
        }
        else
        {
            startTime=document.getElementById("startDate").value;
            endTime=document.getElementById("endDate").value;
        }
    }

    wing = document.getElementById('wingSelection');
    floor = document.getElementById('floorSelection');
    roomnumber = document.getElementById('roomSelection');

    var wingresult = [];
    var floorresult = [];
    var roomnumberresult = [];

    console.log(wing.options.length+" "+floor.options.length+" "+roomnumber.options.length);

    if (wing.options.length > 0) {
        for (var option of wing.options) {
            if (option.selected)
            {
                wingresult.push(option.text);
            }
        }
    }

    if (floor.options.length > 0) {
        for (var option of floor.options) {
            if (option.selected)
            {
                floorresult.push(option.text);
            }
        }
    }

    if (roomnumber.options.length > 0) {
        for (var option of roomnumber.options) {
            if (option.selected)
            {
                roomnumberresult.push(option.text);
            }
        }
    }

    var raw = JSON.stringify({
            "newTickerPriority": priority,
            "wings": wingresult,
            "floors": floorresult,
            "rooms": roomnumberresult,
            "startTime": startTime,
            "endTime": endTime,
            "timeInterval": timeInterval,
            "tickerToken": "K9c491y3kKfuodcuVU8pzxNX1raunlQLFKVqsxJENkE"
        });
    
    // var myHeaders = new Headers();
    // myHeaders.append("Content-Type", "application/json");   

    // console.log(raw);

    // var requestOptions = {
    // method: 'POST',
    // headers: myHeaders,
    // body: raw,
    // redirect: 'follow'
    // };
    // var sysUrl = window.location;
    // fetch(sysUrl.origin+"/ticker/priority-ticker", requestOptions)
    // .then(response => response.text())
    // .then(result => {
    //         const res = JSON.parse(result)
    //         console.log(result)
    //         document.getElementById('notification').innerHTML = res.data
    //     })
    //   .catch(error => console.log('error', error));

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
    "newTickerPriority": "Medium",
    "wings": [],
    "floors": [],
    "rooms": [
        "515"
    ],
    "startTime": "2022-9-26T15:30",
    "endTime": null,
    "timeInterval": "1",
    "tickerToken": "K9c491y3kKfuodcuVU8pzxNX1raunlQLFKVqsxJENkE"
    });

    console.log(raw);

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("https://ticker.dns.army"+"/ticker/priority-ticker", requestOptions)
    .then(response => response.text())
    .then(result => {
        const res = JSON.parse(result)
        console.log(result)
        document.getElementById('notification').innerHTML = res.data
    })
    .catch(error => console.log('error', error));

}


function submitCreateTickerForm() {
    if (validateScheduleForm()){
        document.getElementById("createTickerForm").submit();
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("SubForm").style.display = "inline";
    }
    else
    {alert('HELLO');}
}

var currentTab = 0; 
    showTab(currentTab);
    function showTab(n) {
        var x = document.getElementsByClassName("tab");
        x[n].style.display = "block";
        if (n == 0) {
            document.getElementById("prevBtn").style.display = "none";
            document.getElementById("SubForm").style.display = "none";
        } else {
            document.getElementById("prevBtn").style.display = "inline";
            document.getElementById("SubForm").style.display = "none";
        }
        if (n == (x.length - 1)) {
            document.getElementById("nextBtn").innerHTML = "Schedule";
            document.getElementById("SubForm").style.display = "none";
        } else {
            document.getElementById("nextBtn").innerHTML = "Next";
            document.getElementById("SubForm").style.display = "none";
        }
        fixStepIndicator(n)
    }
    
    function nextPrev(n) {
        var x = document.getElementsByClassName("tab");
        var rex = document.getElementById("nextBtn");
        // alert(n);
        if (n == 1 && !validateForm()) return false;
            x[currentTab].style.display = "none";
            currentTab = currentTab + n;
        // alert(currentTab);
        if (currentTab == 2){
            notification()
            // document.getElementById("nextBtn").style.display = "none";
            // document.getElementById("SubForm").style.display = "inline";
        }
        if (currentTab >= x.length) {
            // document.getElementById("createTickerForm").submit();
            return false;
        }
        showTab(currentTab);
    }

    function validateForm()
    {
        var select = document.getElementById("tickerSelecter");
        var option = select.options[select.selectedIndex];

        var tmp;
    
        if (option.text == "Scrolling Ticker")
        {           
            if (document.getElementById("scrollingTickerTitle").value == "")
            {
                document.getElementById("scrollingTickerTitleLabel").hidden = false;
                return false;
            }
            else
            {
                document.getElementById("scrollingTickerTitleLabel").hidden = true;
                var primaryEnable = document.getElementById("primaryEnable");
                var secondaryEnable = document.getElementById("secondaryEnable");
                var primaryLogoEnabler=document.getElementById("primaryLogoEnabler");

                if (primaryEnable.checked == false && secondaryEnable.checked == false)
                {return false;}
                else if(primaryEnable.checked == true && secondaryEnable.checked == true)
                {
                    if (document.getElementById("primaryTickerMessage").value == "")
                    {
                        document.getElementById("primaryTickerMessageLabel").hidden = false;
                        return false;
                    }
                    else
                    {
                        document.getElementById("primaryTickerMessageLabel").hidden = true;
                        if(primaryLogoEnabler.checked)
                        {
                            tmp=document.getElementById("primaryTickerLogo");
                            if(tmp.files.length == 0 )
                            {
                                document.getElementById("primaryTickerLogoLabel").hidden = false;
                                return false;
                            }
                            else{document.getElementById("primaryTickerLogoLabel").hidden = true;}
                        }
                        if (document.getElementById("secondaryTickerMessage").value == "")
                        {
                            document.getElementById("secondaryTickerMessageLabel").hidden = false;
                            return false;
                        }
                        else
                        {
                            document.getElementById("secondaryTickerMessageLabel").hidden = true;
                            return true;
                        }
                    }
                }
                else if (primaryEnable.checked == true && secondaryEnable.checked == false)
                {
                    if (document.getElementById("primaryTickerMessage").value == "")
                    {
                        document.getElementById("primaryTickerMessageLabel").hidden = false;
                        return false;
                    }
                    else
                    {
                        document.getElementById("primaryTickerMessageLabel").hidden = true;
                        if(primaryLogoEnabler.checked)
                        {
                            tmp=document.getElementById("primaryTickerLogo");
                            if(tmp.files.length == 0 )
                            {
                                document.getElementById("primaryTickerLogoLabel").hidden = false;
                                return false;
                            }
                            else
                            {
                                document.getElementById("primaryTickerLogoLabel").hidden = true;
                                return true;
                            }
                        }
                        else
                        {
                            return true;
                        }
                    }
                }
                else
                {
                    if (document.getElementById("secondaryTickerMessage").value == "")
                    {
                        document.getElementById("secondaryTickerMessageLabel").hidden = false;
                        return false;
                    }
                    else
                    {
                        document.getElementById("secondaryTickerMessageLabel").hidden = true;
                        return true;
                    }
                }
            }
        }
        else if (option.text == "Media Ticker")
        {
            if (document.getElementById("mediaTickerTitle").value == "")
            {
                document.getElementById("mediaTickerTitleLabel").hidden = false;
                return false;
            }
            else
            {
                document.getElementById("mediaTickerTitleLabel").hidden = true;
                var staticEnable = document.getElementById("staticEnable");
                var dynamicEnable = document.getElementById("dynamicEnable");
                if (staticEnable.checked == false && dynamicEnable.checked == false)
                {
                    return false;
                }
                else
                {
                    if (staticEnable.checked)
                    {
                        tmp=document.getElementById("staticTickerLogo");
                        if (tmp.files.length==0)
                        {
                            document.getElementById("staticTickerLogoLabel").hidden = false;
                            return false;
                        }
                        else
                        {
                            document.getElementById("staticTickerLogoLabel").hidden = true;
                            var posbox=document.getElementById("staticPositionBox");
                            option = posbox.options[posbox.selectedIndex];

                            if(option.text=="center")
                            {
                                if(document.getElementById("staticTickerMessage").value=="")
                                {
                                    document.getElementById("staticTickerMessageLabel").hidden = false;
                                    return false;
                                }
                                else
                                {
                                    let imageTag=document.getElementById("staticTickerLogo");
                                    alert(document.getElementById("staticTickerLogo").clientWidth);
                                    if (imageTag.clientWidth!=imageTag.clientHeight)
                                    {
                                        alert("Please select square image.");
                                        return false;
                                    }
                                    else
                                    {
                                        document.getElementById("staticTickerMessageLabel").hidden = true;
                                        return true;
                                    }
                                }
                            }
                            else if(option.text=="fullscreen")
                            {
                                document.getElementById("staticTickerMessageLabel").hidden = true;
                                return true;
                            }
                            else
                            {
                                if (document.getElementById("StaticScrollingEnable").checked)
                                {
                                    if(document.getElementById("staticScrollingTickerMessage").value=="")
                                    {
                                        document.getElementById("staticScrollingTickerMessageLabel").hidden = false;
                                        return false;
                                    }
                                    else
                                    {
                                        document.getElementById("staticScrollingTickerMessageLabel").hidden = true;
                                        return true;
                                    }
                                }
                                else{return true;}
                            }
                        }
                    }
                    else
                    {
                        tmp=document.getElementById("dynamicTickerVideo");
                        if (tmp.files.length==0)
                        {
                            document.getElementById("dynamicTickerVideoLabel").hidden = false;
                            return false;
                        }
                        else
                        {
                            document.getElementById("dynamicTickerVideoLabel").hidden = true;
                            return true;
                        }

                        // {% comment %} alert("1");
                        // if ((dynamicEnable == true)  && (document.getElementById("dynamicTickerVideo").value == undefined))
                        // {return false;}
                        // else
                        // {return true;} {% endcomment %}
                    }
                }
            }
        }
        else if (option.text == "Emergency Ticker")
        {
            if (document.getElementById("emergencyTickerTitle").value == "")
            {
                document.getElementById("emergencyTickerTitleLabel").hidden = false;
                return false;
            }
            else
            {
                document.getElementById("emergencyTickerTitleLabel").hidden = true;
                var emergencyselector = document.getElementById("emergencySelecter");
                var custom = emergencyselector.options[emergencyselector.selectedIndex];
                if (custom.text == "Custom" && document.getElementById("emergencyTickerFile").value == "")
                {return false;}
                else{return true;}
            }
        }
        else
        {
            return false;
        }
    }
    
    function validateScheduleForm() {
        var roomType=document.getElementById("roomTypeSelection");
        var wings=document.getElementById("wingSelection");
        var floor=document.getElementById("floorSelection");
        var rooms=document.getElementById("roomSelection");

        if ( roomType.options.length > 0 || wings.options.length > 0 || floor.options.length > 0 || rooms.options.length > 0)
        {
            return true;
        }
        else
        {
            return false;
        }
      }

    function validateFormf(){
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    for (i = 0; i < y.length; i++) {
        if (y[i].value == "") {
        y[i].className += " invalid";
        valid = false;
        }
    }
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid;
    }
    function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
    }

$("#roomTypeSelection").select2({
    placeholder:'Select Room Type'
});
$("#wingSelection").select2({
    placeholder:'Select Wing'
});
$("#floorSelection").select2({
    placeholder:'Select Floor'
});
$("#roomSelection").select2({
    placeholder:'Select Room Key'
});