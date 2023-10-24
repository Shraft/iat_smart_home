import time
import paho.mqtt.client as mqtt
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_restful import Api
from flask import Flask, render_template, redirect
from routes import Basic
import json

app = Flask(__name__)
websocket = SocketIO(app)
api=Api(app)
app.secret_key = 'your_secret_key'

global_sensors = {}


def mqtt_on_message_callback(client, userdata, message):
    decoded_message = message.payload.decode('utf-8')
    print("Nachricht erhalten: " + decoded_message)

    try:
        sensor_data = json.loads(decoded_message)
        print(type(sensor_data))
    except json.JSONDecodeError as e:
        print("Fehler beim Decodieren der Nachricht:", e)
        return

    if sensor_data["operation"] == "update":
        print("update")
        if sensor_data["uuid"] not in global_sensors:
            print("add sensor")
            global_sensors[sensor_data["uuid"]] = sensor_data["value"]
        

    
    print(global_sensors)



def start_mqtt():
    broker_address = "localhost"       

    client = mqtt.Client("master")         
    client.on_message = mqtt_on_message_callback         

    client.connect(broker_address)          
    client.loop_start()                                                      

    client.subscribe("house/main")         

    client.publish("house/main", "Die Zentrale ist jetzt online")  


    #client.loop_stop()                     
    #sclient.disconnect()                   



# wenn die Datei main.py heist, dann rufe die main() Funktion auf
@websocket.on('connect')
def on_connect(auth):
    print("new Connection")
    websocket.emit("connect", "Connection established")

@websocket.on('get_sensor_data')
def on_connect(auth):
    print("Sensor Data requested")
    websocket.emit("connect", json.dumps(global_sensors))


api.add_resource(Basic, '/')
    
if __name__ == '__main__':
    start_mqtt()
    websocket.run(app, host='0.0.0.0', port=8080, debug=False) 