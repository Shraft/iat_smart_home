function delete_sensor(uuid, current_name) {

    var msg_dict = {}

    msg_dict["uuid"] = uuid;

    console.log(JSON.stringify(msg_dict))

    websocket.emit("delete_sensor", JSON.stringify(msg_dict))
    websocket.emit("get_sensors","")
}