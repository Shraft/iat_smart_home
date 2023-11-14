function rename_sensor(uuid, current_name) {


    var new_name = prompt("Neuer Sensorname:", current_name);

    var msg_dict = {}

    if (new_name == null || new_name == "") {
        alert("Fehlerhafte eingabe")
        return
    }

    msg_dict["uuid"] = uuid;
    msg_dict["new_name"] = new_name;

    console.log(JSON.stringify(msg_dict))

    websocket.emit("rename_sensor", JSON.stringify(msg_dict))
    websocket.emit("get_sensors","")
}