const websocket = io.connect('http://localhost:8080');
var global_view = "overview"

websocket.on('connect', function(data) {
    console.log(data)
});

function ws_send(content){
    if (content == "get_overview") {
        global_view = "overview"
    } else if (content == "get_sensors") {
        global_view = "sensors"
    }
    document.getElementById("sensorcontainer").innerHTML = "";
    websocket.emit(content,"")
}



/* #################################
    List All Sensors to rename them
#################################### */
websocket.on('sensors', function(data) {
    if (global_view != "sensors") {
        return
    }

    sensor_list = JSON.parse(data)
    console.log(sensor_list) 

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

        let img = document.createElement("td")
        let rename_img = new Image();
        rename_img.src = "../static/img/bleistift.png"
        rename_img.classList.add("sensor_actions")
        rename_img.onclick = function() {rename_sensor(sensor_list[sensor_object]["uuid"], sensor_list[sensor_object]["name"]);}
        img.appendChild(rename_img)

        tr_sensor.id = "renaming_" + sensor_list[sensor_object]["type"]

        tr_sensor.appendChild(uuid)
        tr_sensor.appendChild(type)
        tr_sensor.appendChild(name)
        tr_sensor.appendChild(img)
        table.appendChild(tr_sensor)

    }

    sensor_container.appendChild(table)
})


/* #################################
    Show Temperatur Sensors
#################################### */
websocket.on('temp_sensor_data', function(data) {
    if (global_view != "overview") {
        return
    }

    sensor_list = JSON.parse(data)
    console.log(sensor_list)

    const temp_sensors_div = document.getElementById("temp_sensors");
    // IF TempSensor div existiert schon
    if (temp_sensors_div != null) {
        temp_sensors_div.innerHTML = "";
        sensor_element = document.getElementById("temp_sensors")
    // IF TempSensor div existiert noch nicht    
    } else {
        var sensor_element = document.createElement("div")
        sensor_element.id = "temp_sensors";  
        sensor_element.classList.add("sensorelement");
    }
    var parent = document.getElementById("sensorcontainer")

    var caption = document.createElement("h2")
    caption.innerHTML = "Temperatur-Sensoren"
    var sensors = document.createElement("div")

    for (let sensor_object in sensor_list) {
        var trennung = document.createElement("hr")
        var sensor_div = document.createElement("details")
        sensor_div.id = sensor_list[sensor_object]["uuid"]
        var temp_caption = document.createElement("summary")
        temp_caption.innerHTML = sensor_list[sensor_object]["name"] + ": " + sensor_list[sensor_object]["value"] + "°C"
        console.log(sensor_list[sensor_object]["name"])
        sensors.appendChild(trennung)
        sensors.appendChild(sensor_div)
        
        sensor_div.appendChild(temp_caption)
        

        console.log("image")
        var chart = document.createElement("iframe")
        chart.classList.add("chart")
        var chart_string = "../static/charts/" + sensor_object + ".html"
        console.log(chart_string)
        chart.src = chart_string
        sensor_div.appendChild(chart)
       
    }

    sensor_element.appendChild(caption)
    sensor_element.appendChild(sensors)
    parent.appendChild(sensor_element)
});


/* #################################
    Show Light Sensors
#################################### */
websocket.on('light_sensor_data', function(data) {
    if (global_view != "overview") {
        return
    }

    sensor_list = JSON.parse(data)
    console.log("new light sensor data")
    console.log(sensor_list)

    const light_sensors_div = document.getElementById("light_sensors");
    if (light_sensors_div != null) {
        light_sensors_div.innerHTML = "";
        sensor_element = document.getElementById("light_sensors")
    } else {
        var sensor_element = document.createElement("div")
        sensor_element.id = "light_sensors";  
        sensor_element.classList.add("sensorelement");
    }
    var parent = document.getElementById("sensorcontainer")

    var caption = document.createElement("h2")
    caption.innerHTML = "Helligkeits-Sensoren"
    var sensors = document.createElement("div")

    for (let sensor_object in sensor_list) {
        var sensor_div = document.createElement("div")
        sensor_div.id = sensor_list[sensor_object]["uuid"]
        var trennung = document.createElement("hr")
        var temp_caption = document.createElement("p")
        temp_caption.innerHTML = sensor_list[sensor_object]["name"] + ": " + sensor_list[sensor_object]["value"] + "% Licht"
        console.log(sensor_list[sensor_object]["name"])
        sensors.appendChild(sensor_div)
        sensor_div.appendChild(trennung)
        sensor_div.appendChild(temp_caption)
               
    }

    sensor_element.appendChild(caption)
    sensor_element.appendChild(sensors)
    parent.appendChild(sensor_element)
});



/* #################################
    Show RFID Persons
#################################### */
websocket.on('rfid_data', function(data) {
    if (global_view != "overview") {
        return
    }

    sensor_list = JSON.parse(data)
    console.log("new rfid data")
    console.log(sensor_list)

    const rfid_persons_div = document.getElementById("rfid_persons");
    if (rfid_persons_div != null) {
        rfid_persons_div.innerHTML = "";
        sensor_element = document.getElementById("rfid_persons")
    } else {
        var sensor_element = document.createElement("div")
        sensor_element.id = "rfid_persons";  
        sensor_element.classList.add("sensorelement");
    }
    var parent = document.getElementById("sensorcontainer")

    var caption = document.createElement("h2")
    caption.innerHTML = "Personen im Haus"

    var table_div = document.createElement("div")
    var trennung = document.createElement("hr")
        
    var table = document.createElement("table")
    table.classList.add("rfid_table")
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
        value.innerHTML = sensor_list[sensor_object]["value"]

        tr_sensor.appendChild(bild)
        tr_sensor.appendChild(name)
        tr_sensor.appendChild(value)
        table.appendChild(tr_sensor)

    }             

    table_div.appendChild(table)
    sensor_element.appendChild(caption)
    sensor_element.appendChild(trennung)
    sensor_element.appendChild(table_div)
    parent.appendChild(sensor_element)

    
});