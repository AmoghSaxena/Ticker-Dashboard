function getdata() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var javaobj = JSON.parse(xhttp.response);
            // roomtype = document.getElementById('roomtype');
            wing = document.getElementById('wingSelection');
            floor = document.getElementById('floorSelection');
            roomnumber = document.getElementById('roomSelection');
            const arr = []
            for (var i = 0; i < javaobj.data.length; i++) {
                var opt;
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

function alldataremove(id) {
    if (id == "roomSelection") {
        var select = document.getElementById("roomSelection");
        var length = select.options.length;
        for (i = length - 1; i >= 0; i--) {
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
}

function filterforkeys(id) {
    wing = document.getElementById('wingSelection');
    floor = document.getElementById('floorSelection');
    roomnumber = document.getElementById('roomSelection');

    var option;
    var selected = [];


    var request = new XMLHttpRequest();


    if (id == "roomSelection") {
        for (var option of document.getElementById('roomSelection').options) {
            if (option.selected && option.text != 'All') {
                //var request = new XMLHttpRequest();
                request.open("GET", "/static/resources/resource.json", false);
                request.send(null)
                var javaobj = JSON.parse(request.responseText);

                for (var i = 0; i < javaobj.data.length; i++) {

                    if (option.text == javaobj.data[i].key_number && option.text != 'All') {
                        // alert(javaobj.data[i].key_category_name);
                        //   document.getElementById('roomtype').value = javaobj.data[i].key_category_name;
                        document.getElementById('floorSelection').value = javaobj.data[i].floor_name;
                        document.getElementById('wingSelection').value = javaobj.data[i].wing_name;
                    }
                }
            }
        }
    } else if (id == "floorSelection") {
        alldataremove("roomSelection");
        for (var option of document.getElementById('floorSelection').options) {
            if (option.selected && option.text != 'All') {
                //var request = new XMLHttpRequest();
                request.open("GET", "/static/resources/resource.json", false);
                request.send(null)
                var javaobj = JSON.parse(request.responseText);

                for (var i = 0; i < javaobj.data.length; i++) {

                    if (option.text == javaobj.data[i].floor_name && option.text != 'All') {
                        // alert(javaobj.data[i].key_category_name);
                        //   document.getElementById('roomtype').value = javaobj.data[i].key_category_name;
                        document.getElementById('wingSelection').value = javaobj.data[i].wing_name;

                        opt = document.createElement('option');
                        opt.innerHTML = javaobj.data[i].key_number;
                        roomnumber.appendChild(opt);
                    }
                }
            }
        }
    } else if (id == "wingSelection") {
        alldataremove("roomSelection");
        alldataremove("floorSelection")
        for (var option of document.getElementById('wingSelection').options) {
            if (option.selected && option.text != 'All') {
                //var request = new XMLHttpRequest();
                request.open("GET", "/static/resources/resource.json", false);
                request.send(null)
                var javaobj = JSON.parse(request.responseText);

                for (var i = 0; i < javaobj.data.length; i++) {

                    if (option.text == javaobj.data[i].wing_name && option.text != 'All') {
                        // alert(javaobj.data[i].key_category_name);
                        //   document.getElementById('roomtype').value = javaobj.data[i].key_category_name;
                        //document.getElementById('wingselection').value = javaobj.data[i].wing_name;

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
    }

}