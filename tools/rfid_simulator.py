import time
import paho.mqtt.client as mqtt
import json
import random
import argparse

persons_count = 0

person = random.randint(100000, 999999)

broker = "localhost"
client = mqtt.Client(f"rfid_sender-{person}")

# Last will implementation
last_will_data = {"uuid": person,
                        "type": "rfid",
                        "operation" : "last_will",
                        "value": "error"}
client.will_set("house/rfid", json.dumps(last_will_data), qos=2)

# foreverloop
counter = 0
send_delay = 10
recon_time = 30
while True:
    counter += 1

    if counter == 1:
        client.connect(broker)
        client.subscribe("house/rfid")
        print(f"Sender aktiviert mit UUID {person}")
    elif counter == int(recon_time/send_delay):
        client.disconnect()
        print("disconnect")
        counter = 0
        continue

    sensor_data = {"type": "rfid",
                    "operation" : "update",
                    "uuid": person}
    client.publish("house/rfid", json.dumps(sensor_data), qos=1)
    print(sensor_data)

    time.sleep(send_delay)