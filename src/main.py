import time
import threading
import paho.mqtt.client as mqtt
from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api
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

# mqtt message outgoing
mqtt_message_queue = []


# ----------------------------------------------------------------------------------------------------------------------
# MQTT MSG income functions
# ----------------------------------------------------------------------------------------------------------------------
def mqtt_on_message_callback(client, userdata, message):
    # Decode Message from MQTT
    decoded_message = message.payload.decode('utf-8')
    try:
        sensor_data = json.loads(decoded_message)
    except json.JSONDecodeError as e:
        print("Fehler beim Decodieren der Nachricht:", e)
        return
    
    print(decoded_message)
    
    # Wenn nicht für Zentrale
    if "addressee" in sensor_data:
        if sensor_data["addressee"] == "slave":
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
    # for temp and light
    if (db_sensor_existing.sensor_type == "temp" or db_sensor_existing.sensor_type =="light"):
        if sensor_data["value"] != "error":
            local_sensor_dict["value"] = round(sensor_data["value"],1)
        else:
            local_sensor_dict["value"] = sensor_data["value"]

    # for rfid
    elif (db_sensor_existing.sensor_type == "rfid"):
        if sensor_data["uuid"] in global_rfid_persons:
            if (sensor_data["operation"] == "last_will"):
                local_sensor_dict["value"] = "error"
            elif global_rfid_persons[sensor_data["uuid"]]["value"] == "offline":
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
    if (sensor_data["operation"] == "last_will") and (sensor_data["value"] == "error"):
        return

    current_sensor = database.query(Sensors).filter(Sensors.uuid == sensor_data["uuid"]).first()
    now = datetime.datetime.now()
    formatted_time = now.strftime("%d %H %M")
    last_sensor_logs = database.query(Sensor_logs).filter(Sensor_logs.sid == current_sensor.sid).all()
    for sensor_object in last_sensor_logs:
        if sensor_object.time == formatted_time:
            pass
        
    new_sensor_commit = Sensor_logs(sid = current_sensor.sid,
                                    time = formatted_time, 
                                    value = round(sensor_data["value"],1) if "value" in sensor_data != None else "empty")
    database.add(new_sensor_commit)
    database.commit()

def on_disconnect(client, userdata, rc):
   print("verbindung verloren")



def start_mqtt():
    # start mqtt
    broker_address = "localhost"       
    client = mqtt.Client("master")         
    client.on_message = mqtt_on_message_callback   
    client.on_disconnect = on_disconnect      
    client.connect(broker_address)          
    #client.loop_start()                                                      
    client.subscribe("house/#")         
    client.publish("house/main", "Die Zentrale ist jetzt online")  

    while True:
        client.loop()
        if len(mqtt_message_queue) != 0:
            client.publish("house/main", json.dumps(mqtt_message_queue[0]))
            mqtt_message_queue.pop(0)
        #time.sleep(1)


# ----------------------------------------------------------------------------------------------------------------------
# Websocket functions
# ----------------------------------------------------------------------------------------------------------------------
@websocket.on('connect')
def on_connect(auth):
    print("new Connection")
    websocket.emit("connect", "Connection established")

@websocket.on('get_sensor_data')
@websocket.on('get_overview')
def on_get_sensor_data(auth):
    print(f"WS: emit infos {global_temp_sensors}")
    if global_temp_sensors:
        websocket.emit("temp_sensor_data", json.dumps(global_temp_sensors))
    if global_light_sensors:
        websocket.emit("light_sensor_data", json.dumps(global_light_sensors))
    if global_rfid_persons:
        websocket.emit("rfid_data", json.dumps(global_rfid_persons))


@websocket.on('get_sensors')
def get_sensors(auth):
    sensor_list = database.query(Sensors).all()
    response_dict = {}
    
    for sensor in sensor_list:
        response_dict[sensor.uuid] = {"type": sensor.sensor_type,
                                      "uuid": sensor.uuid,
                                      "name": sensor.name}
    
    print(f"WS: emit sensors {response_dict}")

    websocket.emit("sensors", json.dumps(response_dict))

@websocket.on('rename_sensor')
def rename_sensor(auth):
    data = json.loads(auth)
    print(f"sensor umbenennen: {data['uuid']} mit {data['new_name']}")

    db_sensor = database.query(Sensors).filter(Sensors.uuid == data["uuid"]).first()
    db_sensor.name = data["new_name"]
    database.commit

    if data["uuid"] in global_light_sensors:
        global_light_sensors[data["uuid"]]["name"] = data["new_name"] 
    if data["uuid"] in global_rfid_persons:
        global_rfid_persons[data["uuid"]]["name"] = data["new_name"]
    if data["uuid"] in global_temp_sensors:
        global_temp_sensors[data["uuid"]]["name"] = data["new_name"] 


@websocket.on('set_rgb')
def set_rgb(auth):
    data = json.loads(auth)
    mqtt_message_queue.append(data)


# ----------------------------------------------------------------------------------------------------------------------
# Main initialazing
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    game_loop_thread = threading.Thread(target=start_mqtt)
    game_loop_thread.daemon = True
    game_loop_thread.start()

    diagram_thread = threading.Thread(target=create_diagrams, args=(database,))
    diagram_thread.daemon = True
    diagram_thread.start()

    websocket.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True) 