const websocket = io.connect('http://localhost:8080');

websocket.on('connect', function(data) {
    console.log(data)
});



websocket.on('enemy_ships', function(data) {
    var enemy_shiplist = JSON.parse(data)
    document.getElementById("insertenemyshipshere").innerHTML = "";
    enemy_ships = []

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