function foselector()
  {
    select = document.getElementById("tickerSelecter");
    option = select.options[select.selectedIndex];
  
    if (option.text == "Scrolling Ticker")
    {
      document.getElementById("scrolling").hidden = false;
      document.getElementById("media").hidden = true;
      document.getElementById("emergency").hidden = true;
      document.getElementById("scheduleEnabler").checked = false;
      document.getElementById("scheduleEnabler").disabled = false;
      document.getElementById("scrollingTickerPriority").value = "Medium";
      foenabler("scheduleEnabler");
    }
    else if (option.text == "Media Ticker")
    {
      document.getElementById("scrolling").hidden = true;
      document.getElementById("media").hidden = false;
      document.getElementById("emergency").hidden = true;
      document.getElementById("scheduleEnabler").checked = false;
      document.getElementById("scheduleEnabler").disabled = false;
      document.getElementById("mediaTickerPriority").value = "Medium";
      foenabler("scheduleEnabler");
    }
    else if (option.text == "Emergency Ticker")
    {
      document.getElementById("scrolling").hidden = true;
      document.getElementById("media").hidden = true;
      document.getElementById("emergency").hidden = false;
      document.getElementById("scheduleEnabler").disabled = true;
      document.getElementById("scheduleEnabler").checked = true;
      foenabler("scheduleEnabler");
    }
    else
    {
      document.getElementById("scrolling").hidden = true;
      document.getElementById("media").hidden = true;
      document.getElementById("emergency").hidden = true;
      document.getElementById("scheduleEnabler").checked = false;
      document.getElementById("scheduleEnabler").disabled = false;
      foenabler("scheduleEnabler");
    }
  }
  
  function foenabler(id)
  {
    var b;
    var e;
    if (id == "primaryEnable")
    {
      b= document.getElementById("primaryEnable");
      if (b.checked)
      {
        document.getElementById("primary").hidden = false;
      }
      else
      {
        document.getElementById("primary").hidden = true;
      }
    }
  
    if (id == "secondaryEnable")
    {
      b= document.getElementById("secondaryEnable");
      if (b.checked)
      {
        document.getElementById("secondary").hidden = false;
      }
      else
      {
        document.getElementById("secondary").hidden = true;
      }
    }
  
    if (id == "staticEnable")
    {
      b= document.getElementById("staticEnable");
      if (b.checked)
      {
        document.getElementById("dynamicEnable").checked = false;
        document.getElementById("dynamic").hidden = true;
        document.getElementById("static").hidden = false;
      }
      else
      {
        document.getElementById("static").hidden = true;
      }
    }
  
    if (id == "dynamicEnable")
    {
      b= document.getElementById("dynamicEnable");
      if (b.checked)
      {
        document.getElementById("staticEnable").checked = false;
        document.getElementById("static").hidden = true;
        document.getElementById("dynamic").hidden = false;
      }
      else
      {
        document.getElementById("dynamic").hidden = true;
      }
    }
  
    if (id == "emergencySelecter") {
          select = document.getElementById("emergencySelecter");
          option = select.options[select.selectedIndex];
          if (option.text == "Custom") {
              document.getElementById("custom").hidden = false;
          } else {
              document.getElementById("custom").hidden = true;
          }
    }
  
    if (id == "scheduleEnabler")
    {
      b=document.getElementById("scheduleEnabler");
      if (b.checked)
      {
        document.getElementById("occurancySection").hidden = true;
        document.getElementById("dateTimeSection").hidden = true;
     }
      else
      {
        document.getElementById("occurancySection").hidden = false;
        document.getElementById("dateTimeSection").hidden = false;
      }
    }
  
    if (id == "onetime")
    {
      b=document.getElementById("onetime");
      if (b.checked)
      {
        document.getElementById("endDate").hidden = true;
        document.getElementById("frequency").hidden = true;
        document.getElementById("days").hidden = true;
      }
      else
      {
        document.getElementById("endDate").hidden = false;
        document.getElementById("frequency").hidden = false;
        document.getElementById("days").hidden = false;
      }
    }
  
    if (id == "recurring")
    {
      b=document.getElementById("recurring");
      if (b.checked)
      {
        document.getElementById("endDate").hidden = false;
        document.getElementById("frequency").hidden = false;
        document.getElementById("days").hidden = false;
      }
      else
      {
        document.getElementById("endDate").hidden = true;
        document.getElementById("frequency").hidden = true;
        document.getElementById("days").hidden = true;
      }
    }
    
  }
  
  function foLoader()
  {
    document.getElementById("scrolling").hidden = true;
    document.getElementById("media").hidden = true;
    document.getElementById("emergency").hidden = true;
    document.getElementById("primary").hidden = true;
    document.getElementById("secondary").hidden = true;
    document.getElementById("static").hidden = true;
    document.getElementById("dynamic").hidden = true;
    document.getElementById("emergency").hidden = true;
    document.getElementById("custom").hidden = true;
    document.getElementById("endDate").hidden = true;
    document.getElementById("frequency").hidden = true;
    document.getElementById("days").hidden = true;
    document.getElementById("primaryLogo").hidden = true;
    document.getElementById("primaryLogoPosition").hidden = true;
    document.getElementById("staticTickerLogo").hidden = true;
    document.getElementById("dynamicTickerLocation").hidden = true;
    getdata();
  }

  function fologoenabler(id)
  {
    var b;
    if (id== "primaryLogoEnabler")
    {
      b=document.getElementById("primaryLogoEnabler");
      if(b.checked)
      {
        document.getElementById("primaryLogo").hidden = false;
        document.getElementById("primaryLogoPosition").hidden = false;
      }
      else
      {
        document.getElementById("primaryLogo").hidden = true;
        document.getElementById("primaryLogoPosition").hidden = true;
      }
    }
    if (id=="staticTickerLogoEnabler")
    {
      b=document.getElementById("staticTickerLogoEnabler")
      if(b.checked)
      {
        document.getElementById("staticTickerLogo").hidden = false;
      }
      else
      {
        document.getElementById("staticTickerLogo").hidden = true;
      }
    }
  }
  
  function profile() {
    var x = document.getElementById("profileContent");
    if (x.style.display === "none") {
      x.style.display = "block";
      document.getElementById("arrowDown").style.transform = 'rotate(90deg)';
    } else {
      x.style.display = "none";
      document.getElementById("arrowDown").style.transform = 'rotate(-90deg)';
    }
  }
  
function Filevalidation(id)
{
    FileTypeChecker(id);
    var fi;
    if (id=="staticTickerLogo")
    {fi = document.getElementById("staticTickerLogo");}

    if (id=="primaryLogo")
    {fi = document.getElementById("primaryLogo");}
    
    if (id=="dynamicTickerVideo")
    {fi = document.getElementById("dynamicTickerVideo");}
    
    if (fi.files.length > 0)
    {
        for (const i = 0; i <= fi.files.length - 1; i++)
        { 
            const fSize = fi.files.item(i).size;
            const file = Math.round((fSize / 1024));
            // The size of the file.
            if (file >= 20480)
            {
                alert("File too Big, please select a file less than 20MB");
                if (id=="staticTickerLogo")
                {
                    document.getElementById("staticTickerLogo").value='';
                }
                if (id=="primaryLogo")
                {
                    document.getElementById("primaryLogo").value='';
                }
                if (id=="dynamicTickerVideo")
                {
                    document.getElementById("dynamicTickerVideo").value='';
                }
            }
        }
    }
}

function FileTypeChecker(id)
{
    if (id=="staticTickerLogo" || id=="primaryLogo")
    {
        var fileInput;

        if (id=="staticTickerLogo")
        {fileInput = document.getElementById("staticTickerLogo").files[0];}

        if(id=="primaryLogo")
        {fileInput = document.getElementById("primaryLogo").files[0];}

        var allowed = ["png"];
        var found = false;

        allowed.forEach(function(extension) {
        if (fileInput.type.match('.'+extension)) {
            found = true;
        }
        })

        if(found) {
        }
        else{
        alert("Allowed file type is PNG");

        if (id=="staticTickerLogo")
        {document.getElementById("staticTickerLogo").value='';}

        if(id=="primaryLogo")
        {document.getElementById("primaryLogo").value='';}        
        }
    }

    if (id=="dynamicTickerVideo")
    {
        var fileInput = document.getElementById("dynamicTickerVideo").files[0];
        var allowed = ["mp4"];
        var found = false;

        allowed.forEach(function(extension) {
        if (fileInput.type.match('.'+extension)) {
            found = true;
        }
        })

        if(found){
        }
        else{
        alert("Allowed file type is MP4");
        document.getElementById("dynamicTickerVideo").value='';
        }
    }

}

function fopositionbox(id)
{
  var select;
  if (id=="staticPositionBox")
  {
    select = document.getElementById("staticPositionBox");
    option = select.options[select.selectedIndex];

    if(option.text == "center")
    {
      document.getElementById("staticTickerLogoEnabler").checked = true;
      fologoenabler("staticTickerLogoEnabler");
      document.getElementById("staticTickerLogoEnabler").disabled = true;
    }
    else
    {
      document.getElementById("staticTickerLogoEnabler").checked = false;
      fologoenabler("staticTickerLogoEnabler");
      document.getElementById("staticTickerLogoEnabler").disabled = false;
    }

  }

  if (id=="dynamicTickerPosition")
  {
    select = document.getElementById("dynamicTickerPosition");
    option = select.options[select.selectedIndex];

    if(option.text == "center")
    {
      document.getElementById("dynamicTickerLocation").hidden = false;
    }
    else
    {
      document.getElementById("dynamicTickerLocation").hidden = true;
    }

  }
}


function getdata() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      if (xhttp.readyState == 4 && xhttp.status == 200) {
          var javaobj = JSON.parse(xhttp.response);
          roomtype = document.getElementById('roomTypeSelection');
          wing = document.getElementById('wingSelection');
          floor = document.getElementById('floorSelection');
          roomnumber = document.getElementById('roomSelection');
          const arr = [];
          for (var i = 0; i < javaobj.data.length; i++) {
              var opt;
              opt = document.createElement('option');
              opt.innerHTML = javaobj.data[i].key_category_name;
              if (!arr.includes(opt.innerHTML)) {
                  roomtype.appendChild(opt);
                  arr.push(opt.innerHTML);
              }
              opt = document.createElement('option');
              opt.innerHTML = javaobj.data[i].wing_name;
              if (!arr.includes(opt.innerHTML)) {
                  wing.appendChild(opt);
                  arr.push(opt.innerHTML);
              }
              opt = document.createElement('option');
              opt.innerHTML = javaobj.data[i].floor_name;
              if (!arr.includes(opt.innerHTML)) {
                  floor.appendChild(opt);
                  arr.push(opt.innerHTML);
              }
              opt = document.createElement('option');
              opt.innerHTML = javaobj.data[i].key_number;
              if (!arr.includes(opt.innerHTML)) {
                  roomnumber.appendChild(opt);
                  arr.push(opt.innerHTML);
              }
          }
      }
  }
  xhttp.open("GET", "/static/resources/resource.json", true);
  xhttp.send();
}


// DVS data filter



// function alldataremove(id) {
//   if (id == "roomSelection") {
//       var select = document.getElementById("roomSelection");
//       var length = select.options.length;
//       for (i = length - 1; i >= 0; i--) {
//           select.options[i] = null;
//       }
//   }
  // if (id == "floorSelection") {
  //     var select = document.getElementById("floorSelection");
  //     var length = select.options.length;
  //     for (i = length - 1; i >= 0; i--) {
  //         select.options[i] = null;
  //     }
  // }
// }

// function filterforkeys(id) {
//   wing = document.getElementById('wingSelection');
//   floor = document.getElementById('floorSelection');
//   roomnumber = document.getElementById('roomSelection');

//   var option;
//   var selected = [];
//   var request = new XMLHttpRequest();

//   if (id == "roomSelection") {
//       for (var option of document.getElementById('roomSelection').options) {
//           if (option.selected && option.text != 'All') {
//               //var request = new XMLHttpRequest();
//               request.open("GET", "/static/resources/resource.json", false);
//               request.send(null)
//               var javaobj = JSON.parse(request.responseText);

//               for (var i = 0; i < javaobj.data.length; i++) {

//                   if (option.text == javaobj.data[i].key_number && option.text != 'All') {
//                       // alert(javaobj.data[i].key_category_name);
//                       //   document.getElementById('roomtype').value = javaobj.data[i].key_category_name;
//                       document.getElementById('floorSelection').value = javaobj.data[i].floor_name;
//                       document.getElementById('wingSelection').value = javaobj.data[i].wing_name;
//                   }
//               }
//           }
//       }
//   } else if (id == "floorSelection") {
//       alldataremove("roomSelection");
//       for (var option of document.getElementById('floorSelection').options) {
//           if (option.selected && option.text != 'All') {
//               //var request = new XMLHttpRequest();
//               request.open("GET", "/static/resources/resource.json", false);
//               request.send(null)
//               var javaobj = JSON.parse(request.responseText);

//               for (var i = 0; i < javaobj.data.length; i++) {

//                   if (option.text == javaobj.data[i].floor_name && option.text != 'All') {
//                       // alert(javaobj.data[i].key_category_name);
//                       //   document.getElementById('roomtype').value = javaobj.data[i].key_category_name;
//                       document.getElementById('wingSelection').value = javaobj.data[i].wing_name;
//                       opt = document.createElement('option');
//                       opt.innerHTML = javaobj.data[i].key_number;
//                       roomnumber.appendChild(opt);
//                   }
//               }
//           }
//       }
//   } else if (id == "wingSelection") {
//       alldataremove("roomSelection");
//       alldataremove("floorSelection")
//       for (var option of document.getElementById('wingSelection').options) {
//           if (option.selected && option.text != 'All') {
//               //var request = new XMLHttpRequest();
//               request.open("GET", "/static/resources/resource.json", false);
//               request.send(null)
//               var javaobj = JSON.parse(request.responseText);

//               for (var i = 0; i < javaobj.data.length; i++) {

//                   if (option.text == javaobj.data[i].wing_name && option.text != 'All') {
//                       // alert(javaobj.data[i].key_category_name);
//                       //   document.getElementById('roomtype').value = javaobj.data[i].key_category_name;
//                       //document.getElementById('wingselection').value = javaobj.data[i].wing_name;

//                       opt = document.createElement('option');
//                       opt.innerHTML = javaobj.data[i].key_number;
//                       roomnumber.appendChild(opt);
//                       opt = document.createElement('option');
//                       opt.innerHTML = javaobj.data[i].floor_name;
//                       floor.appendChild(opt);
//                   }
//               }
//           }
//       }
//   }

// }

