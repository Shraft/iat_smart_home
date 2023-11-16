import time
import paho.mqtt.client as mqtt
import json
import random

persons_count = 0

persons = {"Nils": 123144141,
           "Basti": 55216134,
           "Markus": 88394013}


while True:
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
    keys=list(persons.keys())
    rdm_person_index = random.randint(0, persons_count-1)
    print(keys[rdm_person_index])
    print(persons[keys[rdm_person_index]])

    sensor_data = {"name": keys[rdm_person_index],
                    "type": "rfid",
                    "operation" : "update",
                    "uuid": persons[keys[rdm_person_index]]}
    client.publish("house/main", json.dumps(sensor_data))
    print(sensor_data)

    time.sleep(5)