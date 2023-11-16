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
from diagram import create_diagrams


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
global_light_sensors = {}
global_rfid_persons = {}



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

    
    # Check if Sensor already exists in DB, if not create
    db_sensor = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
    if db_sensor == None:
        new_sensor = Sensors(uuid=sensor_data['uuid'], 
                                name=sensor_data["type"] + "-" + str(sensor_data["uuid"]), 
                                sensor_type=sensor_data["type"], renamed=False)
        database.add(new_sensor)
        database.commit()

    # Update local Sensor Dict
    # TODO: eventuell ganz darauf verzichten, alles nur mit DB? Basti fragen!
    db_sensor_existing = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
    local_sensor_dict = {"uuid": sensor_data["uuid"],
                "name": db_sensor_existing.name,
                "sensor_type": db_sensor_existing.sensor_type}
    if (db_sensor_existing.sensor_type == "temp" or db_sensor_existing.sensor_type =="light"):
        local_sensor_dict["value"] = sensor_data["value"]
    elif (db_sensor_existing.sensor_type == "rfid"):
        if sensor_data["uuid"] in global_rfid_persons:
            if global_rfid_persons[sensor_data["uuid"]]["value"] == "offline":
                local_sensor_dict["value"] = "online"
            else:
                local_sensor_dict["value"] = "offline"
        else:
            local_sensor_dict["value"] = "online"

    
    # Add current value to correct dictionary
    if local_sensor_dict["sensor_type"] == "temp":
        global_temp_sensors[sensor_data["uuid"]] = local_sensor_dict
    elif local_sensor_dict["sensor_type"] == "light":
        global_light_sensors[sensor_data["uuid"]] = local_sensor_dict
    elif local_sensor_dict["sensor_type"] == "rfid":
        global_rfid_persons[sensor_data["uuid"]] = local_sensor_dict


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
                                    value = sensor_data["value"] if "value" in sensor_data != None else "empty")
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
@websocket.on('get_overview')
def on_get_sensor_data(auth):
    print(f"WS: emit {global_temp_sensors}")
    if global_temp_sensors:
        websocket.emit("temp_sensor_data", json.dumps(global_temp_sensors))
    if global_light_sensors:
        websocket.emit("light_sensor_data", json.dumps(global_light_sensors))
    if global_rfid_persons:
        websocket.emit("rfid_data", json.dumps(global_rfid_persons))


@websocket.on('get_sensors')
def get_sensors(auth):
    print("get sensors requestet")
    sensor_list = database.query(Sensors).all()

    response_dict = {}
    
    for sensor in sensor_list:
        response_dict[sensor.uuid] = {"type": sensor.sensor_type,
                                      "uuid": sensor.uuid,
                                      "name": sensor.name}

    websocket.emit("sensors", json.dumps(response_dict))

@websocket.on('rename_sensor')
def rename_sensor(auth):
    print("sensor umbenennen")
    data = json.loads(auth)

    db_sensor = database.query(Sensors).filter(Sensors.uuid == data["uuid"]).first()
    db_sensor.name = data["new_name"]
    database.commit

# Main initialazing
if __name__ == '__main__':
    game_loop_thread = threading.Thread(target=start_mqtt)
    game_loop_thread.daemon = True
    game_loop_thread.start()

    diagram_thread = threading.Thread(target=create_diagrams, args=(database,))
    diagram_thread.daemon = True
    diagram_thread.start()

    print("Threads gestartet")
    websocket.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True) 