import time
import paho.mqtt.client as mqtt
import json
import random
import argparse

uuid_list = [21344,573215,623456]
sensor_count = 0


parser = argparse.ArgumentParser()
parser.add_argument("--count", help='sensorcount', default=3)
args = parser.parse_args()
arg_count = int(args.count)

while True:
    if arg_count > 0 and arg_count <=3:
        sensor_count = arg_count
        break
    
    eingabe = input("Anzahl Sensoren? [1-3]: ")

    try:
        sensor_count = int(eingabe)  # Du kannst auch int() verwenden, um eine Ganzzahl zu erhalten, wenn gewünscht
    except ValueError:
        print("Invalid Input, repeat")
        continue
    if (sensor_count > 0) and (sensor_count <=3):
        break

broker = "localhost"
client = mqtt.Client("light_sender")
client.connect(broker)
client.subscribe("house/main")
print("Sender aktiviert")


basic_light = 10

while True:
    for sensor_index in range (0, sensor_count):
        basic_light = random.randint(1, 100)

        sensor_data = {"uuid": uuid_list[sensor_index],
                        "type": "light",
                        "operation" : "update",
                        "value": basic_light}
        client.publish("house/main", json.dumps(sensor_data))
        print(sensor_data)

    time.sleep(5)