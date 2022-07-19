var currentTab = 0; 
    showTab(currentTab);
    function showTab(n) {
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
    fixStepIndicator(n)
    }
    
    function nextPrev(n) {
    var x = document.getElementsByClassName("tab");
    if (n == 1 && !validateForm()) return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    if (currentTab >= x.length) {
        document.getElementById("createTickerForm").submit();
        return false;
    }
    showTab(currentTab);
    }
    function validateForm()
    {
        select = document.getElementById("tickerSelecter");
        option = select.options[select.selectedIndex];
    
        if (option.text == "Scrolling Ticker")
        {
            if (document.getElementById("scrollingTickerTitle").value == "")
            {
                return false;
            }
            else
            {return true;}
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
                        if (document.getElementById("staticTickerMessage").value == "")
                        {return false;}
                        else
                        {
                            return true;
                            // {% comment %} alert("1");
                            // if ((document.getElementById("staticTickerLogoEnabler").checked==true) && (document.getElementById("staticTickerLogo").value == undefined))
                            // {alert(2);return false;}
                            // else{alert(3);return true;} {% endcomment %}
                        }
                    }
                    else
                    {
                        return true;
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
                emergencyselector = document.getElementById("emergencySelecter");
                custom = emergencyselector.options[emergencyselector.selectedIndex];
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