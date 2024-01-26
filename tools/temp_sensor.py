import time
import paho.mqtt.client as mqtt
import json
import random

uuid = random.randint(100000, 999999)

def on_disconnect(client, userdata, rc):
   print("verbindung verloren")


broker = "localhost"
client = mqtt.Client(f"temp_sender-{uuid}")
client.on_disconnect = on_disconnect

# Last will implementation
last_will_data = {"uuid": uuid,
                        "type": "temp",
                        "operation" : "last_will",
                        "value": "error"}
client.will_set("house/temp", json.dumps(last_will_data), qos=2)

counter = 0
basic_temp = 10
send_delay = 2
recon_time = 30
while True:
    counter += 1

    if counter == 1:
        client.connect(broker)
        client.subscribe("house/temp")
        print(f"Sender aktiviert mit UUID {uuid}")
    elif counter == int(recon_time/send_delay):
        client.disconnect()
        print("disconnect")
        counter = 0
        continue

    temp_trend = random.randint(0, 2)
    basic_temp = basic_temp - 0.5 if temp_trend == 0 else basic_temp + 0.5

    sensor_data = {"uuid": uuid,
                    "type": "temp",
                    "operation" : "update",
                    "value": basic_temp}
    msg = client.publish("house/temp", json.dumps(sensor_data), qos=1)
    print(msg)

    time.sleep(send_delay)

