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

# init Flask
app = Flask(__name__)
websocket = SocketIO(app)
api=Api(app)
app.secret_key = 'your_secret_key'

# set all http routes
api.add_resource(Basic, '/')

# init DB connection
HOST_IP = "localhost"
db_string = f"postgresql://praktikum:praktikum@{HOST_IP}:9876/smarthome"
engine = create_engine(db_string)
engine.connect()
Session = sessionmaker()
database = Session(bind=engine)

# set global sensors
global_temp_sensors = {}

# -------------------
# MQTT MSG income functions
# -------------------


def mqtt_on_message_callback(client, userdata, message):

    # Decode Message from MQTT
    decoded_message = message.payload.decode('utf-8')
    try:
        sensor_data = json.loads(decoded_message)
    except json.JSONDecodeError as e:
        print("Fehler beim Decodieren der Nachricht:", e)
        return

    # Get Operation of Message
    if sensor_data["operation"] == "update":

        # Check if Sensor already exists in DB, if not create
        db_sensor = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
        if db_sensor == None:
            new_sensor = Sensors(uuid=sensor_data['uuid'], 
                                 name="Sensor-" + str(sensor_data["uuid"]), 
                                 sensor_type="tmp")
            database.add(new_sensor)
            database.commit()
            print(f"Sensor mit UUID: {sensor_data['uuid']} wurde der DB zugeführt")

        # Update local Sensor Dict
        # TODO: eventuell ganz darauf verzichten, alles nur mit DB? Basti fragen!
        db_sensor_existing = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
        sensor_dict = {"uuid": sensor_data["uuid"],
                    "value": sensor_data["value"],
                    "name": db_sensor_existing.name}
        global_temp_sensors[sensor_data["uuid"]] = sensor_dict

        # Write Logs if Necessary
        current_sensor = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
        now = datetime.datetime.now()
        formatted_time = now.strftime("%d %H %M")
        last_sensor_logs = database.query(Sensor_logs).filter(Sensor_logs.sid == current_sensor.sid).all()
        for sensor_object in last_sensor_logs:
            if sensor_object.time == formatted_time:
                pass
                #return
            
        new_sensor_commit = Sensor_logs(sid = current_sensor.sid,
                                        time = formatted_time, 
                                        value = sensor_data["value"])
        database.add(new_sensor_commit)
        database.commit()



def start_mqtt():
    # start mqtt
    broker_address = "localhost"       
    client = mqtt.Client("master")         
    client.on_message = mqtt_on_message_callback         
    client.connect(broker_address)          
    client.loop_start()                                                      
    client.subscribe("house/main")         
    client.publish("house/main", "Die Zentrale ist jetzt online")  

    while True:
        pass

    client.loop_stop()                     
    sclient.disconnect()                   



# -------------------
# Websocket functions
# -------------------

@websocket.on('connect')
def on_connect(auth):
    print("new Connection")
    websocket.emit("connect", "Connection established")

@websocket.on('get_sensor_data')
def on_get_sensor_data(auth):
    websocket.emit("temp_sensor_data", json.dumps(global_temp_sensors))


@websocket.on('get_sensor_history')
def on_get_sensor_history(auth):
    db_temp_sensors = database.query(Sensors).filter(Sensors.sensor_type == "tmp").all()
    db_sensors_history = database.query(Sensor_logs).all()

    temp_sensors_value_history = {}

    if db_temp_sensors == None or db_sensors_history == None:
        return

    for temp_sensor in db_temp_sensors:
        for any_sensor in db_sensors_history:
            if temp_sensor.sid == any_sensor.sid:
                if temp_sensor.uuid in temp_sensors_value_history:
                    value_list = temp_sensors_value_history[temp_sensor.uuid]
                    value_list.append(any_sensor.value)
                else:
                    value_list = []
                    value_list.append(any_sensor.value)
                    temp_sensors_value_history[temp_sensor.uuid] = value_list

    websocket.emit("temp_sensor_history", json.dumps(temp_sensors_value_history))




# Main initialazing
if __name__ == '__main__':
    game_loop_thread = threading.Thread(target=start_mqtt)
    game_loop_thread.daemon = True
    game_loop_thread.start()
    print("Thread gestartet")
    websocket.run(app, host='0.0.0.0', port=8080, debug=False) 