function meineSchleife() {
    console.log("get data from server");
    websocket.emit("get_sensor_data", "")
}

// Die Schleife alle 3 Sekunden starten
setInterval(meineSchleife, 3000);