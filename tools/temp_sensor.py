import time
import paho.mqtt.client as mqtt
import json
import random
import argparse

uuid_list = [44444,55555,66666,77777,88888]
sensor_count = 0

parser = argparse.ArgumentParser()
parser.add_argument("--count", help='sensorcount', default=3)
args = parser.parse_args()
arg_count = int(args.count)

while True:
    if arg_count > 0 and arg_count <=5:
        sensor_count = arg_count
        break
    eingabe = input("Anzahl Sensoren? [1-5]: ")

    try:
        sensor_count = int(eingabe)  # Du kannst auch int() verwenden, um eine Ganzzahl zu erhalten, wenn gewünscht
    except ValueError:
        print("Invalid Input, repeat")
        continue
    if (sensor_count > 0) and (sensor_count <=5):
        break

broker = "localhost"
client = mqtt.Client("temp_sender")
client.connect(broker)
client.subscribe("house/main")
print("Sender aktiviert")


basic_temp = 10

while True:
    temp_trend = random.randint(0, 2)
    target_sensor = random.randint(1, sensor_count)
    basic_temp = basic_temp - 0.5 if temp_trend == 0 else basic_temp + 0.5

    sensor_data = {"uuid": uuid_list[target_sensor-1],
                    "type": "temp",
                    "operation" : "update",
                    "value": basic_temp}
    client.publish("house/main", json.dumps(sensor_data))
    print(sensor_data)

    time.sleep(1)