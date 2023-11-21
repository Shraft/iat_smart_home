import time
import paho.mqtt.client as mqtt
import json
import random
import argparse

persons_count = 0

persons = [123144141, 55216134, 88394013]


parser = argparse.ArgumentParser()
parser.add_argument("--count", help='sensorcount', default=3)
args = parser.parse_args()
arg_count = int(args.count)

while True:
    if arg_count > 0 and arg_count <=3:
        persons_count = arg_count
        break

    eingabe = input("Anzahl Personen? [1-3]: ")

    try:
        persons_count = int(eingabe)  # Du kannst auch int() verwenden, um eine Ganzzahl zu erhalten, wenn gewünscht
    except ValueError:
        print("Invalid Input, repeat")
        continue
    if (persons_count > 0) and (persons_count <=3):
        break

broker = "localhost"
client = mqtt.Client("rfid_sender")
client.connect(broker)
client.subscribe("house/main")
print("Sender aktiviert")


while True:
    rdm_person_index = random.randint(0, persons_count-1)

    sensor_data = {"type": "rfid",
                    "operation" : "update",
                    "uuid": persons[rdm_person_index]}
    client.publish("house/main", json.dumps(sensor_data))
    print(sensor_data)

    time.sleep(5)