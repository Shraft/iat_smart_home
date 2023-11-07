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
        var sensor_div = document.createElement("div")
        sensor_div.id = sensor_list[sensor_object]["uuid"]
        var trennung = document.createElement("hr")
        var temp_caption = document.createElement("p")
        temp_caption.innerHTML = sensor_list[sensor_object]["name"] + ": " + sensor_list[sensor_object]["value"] + "° Celsius"
        console.log(sensor_list[sensor_object]["name"])
        sensors.appendChild(sensor_div)
        sensor_div.appendChild(trennung)
        sensor_div.appendChild(temp_caption)
    }

    sensor_element.appendChild(caption)
    sensor_element.appendChild(sensors)
    parent.appendChild(sensor_element)
});


websocket.on('temp_sensor_history', function(data) {
    sensor_list = JSON.parse(data)
    
    for (let sensor_object in sensor_list) {
        console.log(sensor_list)
        console.log(sensor_object)

        parent = document.getElementById(sensor_object)
        let canvas = document.createElement("canvas")
        canvas.classList.add("temp_graph")

        let temperaturDaten = sensor_list[sensor_object];
        if (temperaturDaten.length > 10) {
            // Die ersten Elemente entfernen, bis die Liste eine Länge von 10 hat
            temperaturDaten.splice(0, temperaturDaten.length - 10);
        }

        // Canvas-Element und 2D-Kontext abrufen
        const context = canvas.getContext('2d');

        // Funktion zum Zeichnen des Temperaturverlaufs
        function zeichneTemperaturGraph() {
            context.clearRect(0, 0, canvas.width, canvas.height);
        
            const breite = canvas.width;
            const höhe = canvas.height;
            const temperaturMax = 30; // Maximale Temperaturwert, den du anzeigen möchtest
            const schrittY = 5; // Schrittgröße für die Y-Achse
        
            context.strokeStyle = 'blue';
            context.lineWidth = 2;
        
            context.beginPath();
            context.moveTo(0, höhe - (temperaturDaten[0] / temperaturMax) * höhe); // Verwende die volle Höhe
        
            const schritt = breite / (temperaturDaten.length - 1);
        
            for (let i = 0; i < temperaturDaten.length; i++) {
                const x = i * schritt;
                const y = höhe - (temperaturDaten[i] / temperaturMax) * höhe; // Skaliere die Temperatur auf die Canvas-Höhe
                context.lineTo(x, y);
        
                // Zahlen an der Y-Achse (Temperatur)
                //context.font = '12px Arial';
                //context.fillText(temperaturDaten[i] + '°C', 10, y);
        
                // Zahlen an der X-Achse (Zeit)
                context.fillText(i, x, höhe - 5);
            }
        
            context.stroke();
        
            // Beschriftungen für Achsen hinzufügen
            context.font = '14px Arial';
            context.fillText('Temperatur', breite - 40, 10);
            context.fillText('Zeit', breite - 40, höhe - 5);
        
            // Y-Achse-Beschriftungen
            for (let i = 10; i <= temperaturMax; i += schrittY) {
                const y = höhe - (i / temperaturMax) * höhe;
                context.fillText(i + '°C', breite - 40, y);
            }
        }
        

        parent.appendChild(canvas)
        zeichneTemperaturGraph();
    }
});

