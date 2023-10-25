import time
import paho.mqtt.client as mqtt
import json
import random

uuid_list = [44444,55555,66666,77777,88888]


while True:
    eingabe = input("Anzahl Sensoren? [1-5]: ")

    try:
        sensor_count = int(eingabe)  # Du kannst auch int() verwenden, um eine Ganzzahl zu erhalten, wenn gewünscht
    except ValueError:
        print("Invalid Input, repeat")
        continue
    if (sensor_count > 0) and (sensor_count <=5):
        break

broker = "localhost"
client = mqtt.Client("sender")
client.connect(broker)
client.subscribe("house/main")
print("Sender aktiviert")


basic_temp = 10

while True:
    temp_trend = random.randint(0, 2)
    basic_temp = basic_temp - 0.5 if temp_trend == 0 else basic_temp + 0.5

    for sensor_id in range(1, sensor_count+1):
        sensor_data = {"uuid": uuid_list[sensor_id-1],
                       "type": "temperatur",
                       "operation" : "update",
                       "value": basic_temp + sensor_id}
        client.publish("house/main", json.dumps(sensor_data))
        print(sensor_data)

    time.sleep(3)