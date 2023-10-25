function meineSchleife() {
    console.log("get data from server");
    websocket.emit("get_sensor_data", "")
    websocket.emit("get_sensor_history", "")
}

// Die Schleife alle 3 Sekunden starten
setInterval(meineSchleife, 3000);