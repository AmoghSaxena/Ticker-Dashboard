function schedulebuttonenabler(id)
{
    if(id == "scheduleenabler")
    {
        var b = document.getElementById("scheduleenabler");
        if (b.checked)
        {
            document.getElementById("occurancysection").hidden = true;
            document.getElementById("datatimesection").hidden = true;
        }
        else
        {
            document.getElementById("occurancysection").hidden = false;
            document.getElementById("datatimesection").hidden = false;
        }
    }
}

function alldataremove(id)
{
    if (id=="roomSelection")
    {
    var select = document.getElementById("roomSelection");
    var length = select.options.length;
    for (i = length-1; i >= 0; i--) {
        select.options[i] = null;
    }
    }
    if (id == "floorSelection") {
        var select = document.getElementById("floorSelection");
        var length = select.options.length;
        for (i = length - 1; i >= 0; i--) {
            select.options[i] = null;
        }
    }
    if (id=="wingSelection"){
    var select = document.getElementById("wingSelection");
    var length = select.options.length;
    for (i = length - 1; i >= 0; i--) {
        select.options[i] = null;
    }
    }
    if (id=="roomTypeSelection"){
    var select = document.getElementById("roomTypeSelection");
    var length = select.options.length;
    for (i = length - 1; i >= 0; i--) {
        select.options[i] = null;
    }
    }
}

function filterforkeys(id) {
    roomtype = document.getElementById('roomTypeSelection');
    wing = document.getElementById('wingSelection');
    floor = document.getElementById('floorSelection');
    roomnumber = document.getElementById('roomSelection');

    var option;
    var selected = [];


    var request = new XMLHttpRequest();

    request.open("GET", "/static/resources/resource.json", false);
    request.send(null);

    var javaobj = JSON.parse(request.responseText);

    if (id == "roomSelection") {

        if (roomnumber.options.length > 0) {

            for (var option of roomnumber.options) {
                if (option.selected && option.text != 'All') {
                    //var request = new XMLHttpRequest();

                    for (var i = 0; i < javaobj.data.length; i++) {

                        if (option.text == javaobj.data[i].key_number && option.text != 'All') {
                            // alert(javaobj.data[i].key_category_name);
                            document.getElementById('roomTypeSelection').value = javaobj.data[i].key_category_name;
                            document.getElementById('floorSelection').value = javaobj.data[i].floor_name;
                            document.getElementById('wingSelection').value = javaobj.data[i].wing_name;
                        }
                    }
                }
            }
            alert(document.getElementById('roomTypeSelection').attributes);
        } else
        {
            const arr = [];
            var opt;

            for (var i=0; i< javaobj.data.length;i++)
            {
                opt = document.createElement('option');
                opt.innerHTML = javaobj.data[i].key_number;
                if (!arr.includes(opt.innerHTML)) {
                    roomnumber.appendChild(opt);
                    arr.push(opt.innerHTML);
                }
            }


            if (roomtype.options.length == 0){

                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].key_category_name;
                    if (!arr.includes(opt.innerHTML)) {
                        roomtype.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }                    
                }
            }

            if (wing.options.length == 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].wing_name;
                    if (!arr.includes(opt.innerHTML)) {
                        wing.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }

            if (floor.options.length== 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].floor_name;
                    if (!arr.includes(opt.innerHTML)) {
                        floor.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }
        }

    } else if (id == "floorSelection") {
        
        if (floor.options.length > 0) {

            for (var option of floor.options) {
                if (option.selected && option.text != 'All') {
                    //var request = new XMLHttpRequest();

                    for (var i = 0; i < javaobj.data.length; i++) {

                        if (option.text == javaobj.data[i].floor_name && option.text != 'All') {
                            // alert(javaobj.data[i].key_category_name);
                            document.getElementById('roomTypeSelection').value = javaobj.data[i].key_category_name;
                            document.getElementById('wingSelection').value = javaobj.data[i].wing_name;

                            alldataremove("roomSelection");

                            opt = document.createElement('option');
                            opt.innerHTML = javaobj.data[i].key_number;
                            roomnumber.appendChild(opt);
                        }
                    }
                }
            }

        } 
        else{
            const arr = [];
            var opt;
            
            if (roomtype.options.length == 0){

                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].key_category_name;
                    if (!arr.includes(opt.innerHTML)) {
                        roomtype.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }

            }

            if (wing.options.length == 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].wing_name;
                    if (!arr.includes(opt.innerHTML)) {
                        wing.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }

            for (var i = 0; i < javaobj.data.length; i++)
            {
                opt = document.createElement('option');
                opt.innerHTML = javaobj.data[i].floor_name;
                if (!arr.includes(opt.innerHTML)) {
                    floor.appendChild(opt);
                    arr.push(opt.innerHTML);
                }
            }

            if (roomnumber.options.length== 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].key_number;
                    if (!arr.includes(opt.innerHTML)) {
                        roomnumber.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }
        }

    } else if (id == "wingSelection") {

        if (wing.options.length > 0) {
            for (var option of winglength.options) {
                if (option.selected && option.text != 'All') {
                    //var request = new XMLHttpRequest();
                    alldataremove("roomSelection");
                    alldataremove("floor");

                    for (var i = 0; i < javaobj.data.length; i++) {

                        if (option.text == javaobj.data[i].wing_name && option.text != 'All') {
                            // alert(javaobj.data[i].key_category_name);
                            document.getElementById('roomTypeSelection').value = javaobj.data[i].key_category_name;
                            
                            opt = document.createElement('option');
                            opt.innerHTML = javaobj.data[i].key_number;
                            roomnumber.appendChild(opt);
                            opt = document.createElement('option');
                            opt.innerHTML = javaobj.data[i].floor_name;
                            floor.appendChild(opt);
                        }
                    }
                }
            }
        }else
        {
            const arr = [];
            var opt;

            if (roomtype.options.length == 0){

                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].key_category_name;
                    if (!arr.includes(opt.innerHTML)) {
                        roomtype.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }

            }

            for (var i = 0; i < javaobj.data.length; i++)
            {
                opt = document.createElement('option');
                opt.innerHTML = javaobj.data[i].wing_name;
                if (!arr.includes(opt.innerHTML)) {
                    wing.appendChild(opt);
                    arr.push(opt.innerHTML);
                }
            }

            if (floor.options.length == 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].floor_name;
                    if (!arr.includes(opt.innerHTML)) {
                        floor.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }

            if (roomnumber.options.length== 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].key_number;
                    if (!arr.includes(opt.innerHTML)) {
                        roomnumber.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }
        }
    }
    else if (id == "roomTypeSelection") {

        if (roomtype.options.length > 0) {

            for (var option of roomtype.options) {
                if (option.selected && option.text != 'All') {
                    //var request = new XMLHttpRequest();
                    alldataremove("roomSelection");
                    alldataremove("floorSelection");
                    alldataremove("wingSelection");

                    for (var i = 0; i < javaobj.data.length; i++) {

                        if (option.text == javaobj.data[i].key_category_name && option.text != 'All') {
                            // alert(javaobj.data[i].key_category_name);
                            
                            opt = document.createElement('option');
                            opt.innerHTML = javaobj.data[i].key_number;
                            roomnumber.appendChild(opt);

                            opt = document.createElement('option');
                            opt.innerHTML = javaobj.data[i].floor_name;
                            floor.appendChild(opt);
                            
                            opt = document.createElement('option');
                            opt.innerHTML = javaobj.data[i].wing_name;
                            wing.appendChild(opt);
                        }
                    }
                }
            }
        } else {
            const arr = [];
            var opt;

            for (var i = 0; i < javaobj.data.length; i++)
            {
                opt = document.createElement('option');
                opt.innerHTML = javaobj.data[i].key_category_name;
                if (!arr.includes(opt.innerHTML)) {
                    roomtype.appendChild(opt);
                    arr.push(opt.innerHTML);
                }
            }
                        
            if (wing.options.length == 0){

                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].wing_name;
                    if (!arr.includes(opt.innerHTML)) {
                        wing.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }

            }

            if (floor.options.length == 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].floor_name;
                    if (!arr.includes(opt.innerHTML)) {
                        floor.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }

            if (roomnumber.options.length== 0)
            {
                for (var i = 0; i < javaobj.data.length; i++) {
                    opt = document.createElement('option');
                    opt.innerHTML = javaobj.data[i].key_number;
                    if (!arr.includes(opt.innerHTML)) {
                        roomnumber.appendChild(opt);
                        arr.push(opt.innerHTML);
                    }
                }
            }
        }
    } else {}
}