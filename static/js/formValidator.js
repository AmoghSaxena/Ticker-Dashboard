var currentTab = 0; 
    showTab(currentTab);
    function showTab(n) {
        // alert(n)
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
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("SubForm").style.display = "inline";
    }
    if (currentTab >= x.length) {
        document.getElementById("createTickerForm").submit();
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
                return false;
            }
            else
            {
                var primaryEnable = document.getElementById("primaryEnable");
                var secondaryEnable = document.getElementById("secondaryEnable");
                var primaryLogoEnabler=document.getElementById("primaryLogoEnabler");

                if (primaryEnable.checked == false && secondaryEnable.checked == false)
                {return false;}
                else if(primaryEnable.checked == true && secondaryEnable.checked == true)
                {
                    if (document.getElementById("primaryTickerMessage").value == "")
                    {return false;}
                    else
                    {
                        if(primaryLogoEnabler.checked)
                        {
                            tmp=document.getElementById("primaryTickerLogo");
                            if(tmp.files.length == 0 )
                            {return false;}
                        }
                        if (document.getElementById("secondaryTickerMessage").value == "")
                        {return false;}
                        else
                        {return true;}
                    }
                }
                else if (primaryEnable.checked == true && secondaryEnable.checked == false)
                {
                    if (document.getElementById("primaryTickerMessage").value == "")
                    {return false;}
                    else
                    {
                        if(primaryLogoEnabler.checked)
                        {
                            tmp=document.getElementById("primaryTickerLogo");
                            if(tmp.files.length == 0 )
                            {return false;}
                            else
                            {return true;}
                        }
                        else{return true;}
                    }
                }
                else
                {
                    if (document.getElementById("secondaryTickerMessage").value == "")
                    {return false;}
                    else
                    {return true;}
                }
            }
        }
        else if (option.text == "Media Ticker")
        {
            if (document.getElementById("mediaTickerTitle").value == "")
            {return false;}
            else
            {
                var staticEnable = document.getElementById("staticEnable");
                var dynamicEnable = document.getElementById("dynamicEnable");
                if (staticEnable.checked == false && dynamicEnable.checked == false)
                {return false;}
                else
                {
                    if (staticEnable.checked)
                    {
                        tmp=document.getElementById("staticTickerLogo");
                        if (tmp.files.length==0){return false;}
                        else
                        {
                            var posbox=document.getElementById("staticPositionBox");
                            option = posbox.options[posbox.selectedIndex];

                            if(option.text=="center")
                            {
                                if(document.getElementById("staticTickerMessage").value=="")
                                {return false;}
                                else{return true;}
                            }
                            else if(option.text=="fullscreen")
                            {
                                return true;
                            }
                            else
                            {
                                if (document.getElementById("StaticScrollingEnable").checked)
                                {
                                    if(document.getElementById("staticScrollingTickerMessage").value==""){return false;}
                                    else{return true;}
                                }
                                else{return true;}
                            }
                        }
                    }
                    else
                    {
                        tmp=document.getElementById("dynamicTickerVideo");
                        if (tmp.files.length==0){return false;}
                        else{return true;}

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
                {return false;}
            }
            else
            {
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