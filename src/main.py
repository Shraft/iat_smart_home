import time
import threading
import paho.mqtt.client as mqtt
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_restful import Api
from flask import Flask, render_template, redirect
from routes import Basic
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_tables import Sensor_logs, Sensors
import datetime

app = Flask(__name__)
websocket = SocketIO(app)
api=Api(app)
app.secret_key = 'your_secret_key'

api.add_resource(Basic, '/')


HOST_IP = "localhost"
db_string = f"postgresql://praktikum:praktikum@{HOST_IP}:9876/smarthome"
engine = create_engine(db_string)
engine.connect()
Session = sessionmaker()
database = Session(bind=engine)


global_temp_sensors = {}


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
        
        db_sensor = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
        if db_sensor == None:
            new_sensor = Sensors(uuid=sensor_data['uuid'], name=None, sensor_type="Temperatursensor")
            database.add(new_sensor)
            database.commit()
            print(f"Sensor mit UUID: {sensor_data['uuid']} wurde der DB zugeführt")

        else:
            sensor_name = db_sensor.name
            sensor_dict = {"uuid": sensor_data["uuid"],
                        "value": sensor_data["value"],
                        "name": sensor_name}
            global_temp_sensors[sensor_data["uuid"]] = sensor_dict


            current_sensor = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
            now = datetime.datetime.now()
            formatted_time = now.strftime("%d %H %M")
            last_sensor_logs = database.query(Sensor_logs).filter(Sensor_logs.sid == current_sensor.sid).all()
            for sensor_object in last_sensor_logs:
                if sensor_object.time == formatted_time:
                    return
                
            new_sensor_commit = Sensor_logs(sid = current_sensor.sid, sensor_type = current_sensor.sensor_type,
                                            time = formatted_time, value = sensor_data["value"])
            database.add(new_sensor_commit)
            database.commit()


    #print(global_temp_sensors)



def start_mqtt():
    broker_address = "localhost"       

    client = mqtt.Client("master")         
    client.on_message = mqtt_on_message_callback         

    client.connect(broker_address)          
    client.loop_start()                                                      

    client.subscribe("house/main")         

    client.publish("house/main", "Die Zentrale ist jetzt online")  

    while True:
        pass

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
    websocket.emit("temp_sensor_data", json.dumps(global_temp_sensors))



    
if __name__ == '__main__':

    game_loop_thread = threading.Thread(target=start_mqtt)
    game_loop_thread.daemon = True
    game_loop_thread.start()
    print("Thread gestartet")

    #start_mqtt()
    websocket.run(app, host='0.0.0.0', port=8080, debug=False) 