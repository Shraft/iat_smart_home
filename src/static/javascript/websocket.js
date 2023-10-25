const websocket = io.connect('http://localhost:8080');

websocket.on('connect', function(data) {
    console.log(data)
});

websocket.on('temp_sensor_data', function(data) {
    sensor_list = JSON.parse(data)
    //let sensor_list = {"44444": 3.5, "55555": 4.5}
    console.log(sensor_list)

    document.getElementById("sensorcontainer").innerHTML = "";

    var parent = document.getElementById("sensorcontainer")

    var sensor_element = document.createElement("div")
    sensor_element.id = "temp_sensors";  
    sensor_element.classList.add("sensorelement");
    var caption = document.createElement("h2")
    caption.innerHTML = "Temperatur Sensoren"
    var sensors = document.createElement("div")

    for (let sensor_object in sensor_list) {
        var trennung = document.createElement("hr")
        var temp_caption = document.createElement("p")
        temp_caption.innerHTML = sensor_list[sensor_object]["name"] + ": " + sensor_list[sensor_object]["value"] + "° Celsius"
        console.log(sensor_list[sensor_object]["name"])
        sensors.appendChild(trennung)
        sensors.appendChild(temp_caption)
    }

    sensor_element.appendChild(caption)
    sensor_element.appendChild(sensors)
    parent.appendChild(sensor_element)
});


websocket.on('enemy_ships', function(data) {
    


    // Iterate thought all Ships
    for (let index = 0; index < enemy_shiplist.length; index++) {
        enemy_ships.push(enemy_shiplist[index])   
        enemy_ships[index]["html_image_id"] = "mothership_container" + index
        enemy_ships[index]["local_direction"] = "left"
       
        // Images
        var parent = document.getElementById("insertenemyshipshere")                         // get Insertion-Space
        var ship_element = document.createElement("div");  
        ship_element.id = "enemy_mothership_container" + index;                   
        ship_element.style.top = parseInt(1080 - enemy_shiplist[index].local_position[1]) + "px"
        ship_element.style.left = enemy_shiplist[index].local_position[0] + "px"
        ship_element.classList.add("enemy_ship_container_class")
        
        var ship_image = document.createElement("img");                                 // create Ship Image
        ship_image.id = "enemy_mothership" + index;
        ship_image.style.width = enemy_shiplist[index].size / 3 + "px"
        ship_image.src = "../static/images/ships/" + enemy_shiplist[index].ship_class.toLowerCase() + "_right.png";
        ship_element.appendChild(ship_image)
        parent.appendChild(ship_element)
    }
});