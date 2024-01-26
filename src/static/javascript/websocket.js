const websocket = io.connect('http://localhost:8080');
var global_view = "overview"
var global_details = {}

websocket.on('connect', function(data) {
    console.log(data)
});

function ws_send_on_navigation_change(content){
    if (content == "get_overview") {
        global_view = "overview"
    } else if (content == "get_sensors") {
        global_view = "sensors"
    }
    document.getElementById("sensorcontainer").innerHTML = "";
    websocket.emit(content,"")
}

function prepare_sensor_visualisation(sensorType) {
    if (global_view !== "overview") {
        return null;
    }

    const sensorsDiv = document.getElementById(sensorType);
    var sensorElement;

    // speichere ausgeklappte menus
    var detailsTags = document.querySelectorAll('details');
    detailsTags.forEach(function(detailsTag) {
        if (detailsTag != null){
            global_details[detailsTag.id] = detailsTag.open;
        }
    });

    if (sensorsDiv !== null) {
        sensorsDiv.innerHTML = "";
        sensorElement = document.getElementById(sensorType);
    } else {
        sensorElement = document.createElement("div");
        sensorElement.id = sensorType;
        sensorElement.classList.add("sensorelement");
    }
    return sensorElement;
}

function repair_sensor_visualisation(){
    // hole alle menus
    var detailsTags = document.querySelectorAll('details');
    detailsTags.forEach(function(detailsTag) {
        var tag_value = global_details[detailsTag.id]
        detailsTag.open = tag_value
    });
}




/* #################################
    Show Temperatur Sensors
#################################### */
websocket.on('temp_sensor_data', function(data) {
    sensor_list = JSON.parse(data)

    let sensor_element = prepare_sensor_visualisation("temp_sensors");
    if (sensor_element== null) {return}

    var parent = document.getElementById("sensorcontainer");

    var caption = document.createElement("h2")
    caption.innerHTML = "Temperatur-Sensoren"
    var sensors = document.createElement("div")

    for (let sensor_object in sensor_list) {
        var trennung = document.createElement("hr")
        var sensor_div = document.createElement("details")
        sensor_div.id = sensor_list[sensor_object]["uuid"]
        var temp_caption = document.createElement("summary")

        console.log(sensor_list[sensor_object]["value"])

        // last will if value is error
        if (sensor_list[sensor_object]["value"] != "error") {
            temp_caption.innerHTML = sensor_list[sensor_object]["name"] + ": " + sensor_list[sensor_object]["value"] + "°C"
        } else {
            temp_caption.innerHTML = sensor_list[sensor_object]["name"] + ": " + "Verbindung verloren ...";
        }

        sensors.append(trennung, sensor_div)
        
        sensor_div.appendChild(temp_caption)
        
        var chart = document.createElement("iframe")
        chart.classList.add("chart")
        var chart_string = "../static/charts/" + sensor_object + ".html"
        chart.src = chart_string
        sensor_div.appendChild(chart)
    }
    sensor_element.append(caption, sensors)
    parent.appendChild(sensor_element)

    repair_sensor_visualisation();
});


/* #################################
    Show Light Sensors
#################################### */
function updateColor(r,g,b, uuid) {
    var red = document.getElementById(r).value;
    var green = document.getElementById(g).value;
    var blue = document.getElementById(b).value;
    var colorDisplay = document.getElementById('color-display_' + uuid);
    colorDisplay.style.backgroundColor = 'rgb(' + red + ',' + green + ',' + blue + ')';
    var colorDisplay = document.getElementById('controls_' + uuid);
    colorDisplay.style.borderColor = 'rgb(' + red + ',' + green + ',' + blue + ')';

    var data = {"uuid": uuid, "addressee": "slave",
                "r": red, "g": green, "b": blue}
    websocket.emit("set_rgb", JSON.stringify(data))
}

function insert_rgb_input(uuid) {
    function createSlider(label, id) {
        var sliderLabel = document.createElement("label");
        sliderLabel.innerHTML = label + ":";
        var slider = document.createElement("input");
        slider.type = "range";
        slider.id = id + "_" + uuid;
        slider.min = "0";
        slider.max = "255";
        slider.value = "0";
        return [sliderLabel, slider, document.createElement("br")];
    }

    var controls = Object.assign(document.createElement("div"), { id: "controls_" + uuid, className: "controls" });
    var sliders = Object.assign(document.createElement("div"), { id: "sliders_" + uuid, className: "sliders" });

    var [redLabel, redSlider, redBreak] = createSlider("Red", "red");
    var [greenLabel, greenSlider, greenBreak] = createSlider("Green", "green");
    var [blueLabel, blueSlider, blueBreak] = createSlider("Blue", "blue");

    sliders.append(redLabel, redSlider, redBreak, greenLabel, greenSlider, greenBreak, blueLabel, blueSlider, blueBreak);

    var applyButton = Object.assign(document.createElement("button"), {
        onclick: () => updateColor(`red_${uuid}`, `green_${uuid}`, `blue_${uuid}`, uuid),
        innerHTML: "Übernehmen"
      });
    sliders.appendChild(applyButton);

    var colorDisplay = Object.assign(document.createElement("div"), {className: "color-display", id: `color-display_${uuid}`});
      
    controls.append(sliders, colorDisplay);

    return controls;
}


websocket.on('light_sensor_data', function(data) {
    sensor_list = JSON.parse(data)

    let sensor_element = prepare_sensor_visualisation("light_sensors");
    if (sensor_element== null) {return}

    var parent = document.getElementById("sensorcontainer");
    var caption = Object.assign(document.createElement("h2"), { innerHTML: "Helligkeits-Sensoren" });
    var sensors = document.createElement("div")

    for (let sensor_object in sensor_list) {
        var uuid = sensor_list[sensor_object]["uuid"]
        var sensor_div = document.createElement("div")
        sensor_div.id = uuid
        var trennung = document.createElement("hr")
        var details = document.createElement("details")
        details.id = sensor_list[sensor_object]["uuid"]
        var summary = document.createElement("summary")

        // last will if value is error
        if (sensor_list[sensor_object]["value"] != "error") {
            summary.innerHTML = sensor_list[sensor_object]["name"] + ": " + sensor_list[sensor_object]["value"] + "% Licht"
        } else {
            summary.innerHTML = sensor_list[sensor_object]["name"] + ": " + "Verbindung verloren ...";
        }

        controls = insert_rgb_input(uuid)
        
        sensors.appendChild(sensor_div)
        sensor_div.appendChild(trennung)
        details.append(summary,controls)
        sensors.appendChild(details)
    }

    sensor_element.append(caption,sensors)
    parent.appendChild(sensor_element)

    repair_sensor_visualisation();
});


/* #################################
    Show RFID Persons
#################################### */
websocket.on('rfid_data', function(data) {
    sensor_list = JSON.parse(data)

    let sensor_element = prepare_sensor_visualisation("rfid_persons");
    if (sensor_element== null) {return}

    var parent = document.getElementById("sensorcontainer");
    var caption = Object.assign(document.createElement("h2"), { innerHTML: "Personen im Haus" });
    var table_div = document.createElement("div")
    var trennung = document.createElement("hr")
    var table = Object.assign(document.createElement("table"), { className: "rfid_table" });
    var tr_head = document.createElement("tr")
    var head_string = "<th>Bild</th><th>Name</th><th>Anwesenheit</th>"
    tr_head.innerHTML = head_string;
    table.appendChild(tr_head)

    for (let sensor_object in sensor_list) {

        var tr_sensor = document.createElement("tr") 
        tr_sensor.id = "person_" + sensor_list[sensor_object]["value"]
        var bild = document.createElement("td")
        bild.innerHTML = "<img src='../static/persons/" + sensor_list[sensor_object]["uuid"] + ".jpeg' class='person_img'>"
        var name = document.createElement("td")
        name.innerHTML = sensor_list[sensor_object]["name"]
        var value = document.createElement("td")

        // last will if value is error
        if (sensor_list[sensor_object]["value"] != "error") {
            value.innerHTML = sensor_list[sensor_object]["value"]
        } else {
            value.innerHTML = "Verschollen ...";
        }

        tr_sensor.append(bild,name,value)
        table.appendChild(tr_sensor)
    }             

    table_div.appendChild(table)
    sensor_element.append(caption,trennung,table_div)
    parent.appendChild(sensor_element) 
});




/* #################################
    List All Sensors to rename them
#################################### */
websocket.on('sensors', function(data) {
    if (global_view != "sensors") {
        return
    }
    sensor_list = JSON.parse(data)

    const sensor_container = document.getElementById("sensorcontainer");
    sensor_container.innerHTML = "";

    var table = document.createElement("table")
    table.classList.add("sensorelement_renaming")
    var tr_head = document.createElement("tr")
    var head_string = "<th>UUID</th><th>Type</th><th>Name</th><th>Actions</th>"

    tr_head.innerHTML = head_string;
    table.appendChild(tr_head)

    for (let sensor_object in sensor_list) {
        var tr_sensor = document.createElement("tr") 
        var uuid = document.createElement("td")
        uuid.innerHTML = sensor_list[sensor_object]["uuid"]
        var name = document.createElement("td")
        name.innerHTML = sensor_list[sensor_object]["name"]
        var type = document.createElement("td")
        type.innerHTML = sensor_list[sensor_object]["type"]

        // rename
        let img = document.createElement("td")
        let rename_img = Object.assign(new Image(), {
            src: "../static/img/bleistift.png",
            className: "sensor_actions",
            onclick: function() {rename_sensor(sensor_list[sensor_object].uuid, sensor_list[sensor_object].name);}
          });
        img.appendChild(rename_img)

        tr_sensor.id = "renaming_" + sensor_list[sensor_object]["type"]

        // delete
        let delimg = document.createElement("td")
        let delete_img = Object.assign(new Image(), {
            src: "../static/img/loschen.png",
            className: "sensor_actions",
            onclick: function() {delete_sensor(sensor_list[sensor_object].uuid, sensor_list[sensor_object].name);}
          });
          delimg.appendChild(delete_img)

        tr_sensor.id = "deleting_" + sensor_list[sensor_object]["type"]
        //


        tr_sensor.append(uuid, type, name, img, delimg)
        table.appendChild(tr_sensor)
    }

    sensor_container.appendChild(table)
})