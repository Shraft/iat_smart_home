import time
import paho.mqtt.client as mqtt
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_restful import Api
from flask import Flask, render_template, redirect
from routes import Basic

app = Flask(__name__)
websocket = SocketIO(app)
api=Api(app)
app.secret_key = 'your_secret_key'


def mqtt_on_message_callback(client, userdata, message):
    print("Nachricht erhalten: " + str(message.payload.decode("utf-8")))


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
    websocket.emit("connect", "nice")



api.add_resource(Basic, '/')
    
if __name__ == '__main__':
    start_mqtt()
    websocket.run(app, host='0.0.0.0', port=8080, debug=False) 