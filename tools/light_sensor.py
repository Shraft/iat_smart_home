import time
import paho.mqtt.client as mqtt
import json
import random
import argparse

uuid_list = [21344,573215,623456]
sensor_count = 0


parser = argparse.ArgumentParser()
parser.add_argument("--count", help='sensorcount', default=1)
args = parser.parse_args()
arg_count = int(args.count)


def print_rgb_color(r, g, b, text):
    # ANSI Escape Code für die RGB-Farbe
    color_code = f"\033[38;2;{r};{g};{b}m"

    # ANSI Escape Code für die Standardfarbe (zum Zurücksetzen)
    reset_code = "\033[0m"

    # text additional
    text = "##############################\n\t" + text + "\n##############################"

    # Text mit der angegebenen Farbe ausgeben
    print(f"{color_code}{text}{reset_code}")

# -------------------
# MQTT MSG income functions
# -------------------
def mqtt_on_message_callback(client, userdata, message):

    # Decode Message from MQTT
    decoded_message = message.payload.decode('utf-8')
    try:
        data = json.loads(decoded_message)
    except json.JSONDecodeError as e:
        print("Fehler beim Decodieren der Nachricht:", e)
        return
    
    if "addressee" in data:
        if data["addressee"] == "slave":
            if data["uuid"] in uuid_list:
                print_rgb_color(data["r"],data["g"], data["b"], f"Sensor-{data['uuid']}")
    

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
client.on_message = mqtt_on_message_callback  

# Last will implementation
last_will_data = {"uuid": uuid_list[0],
                        "type": "light",
                        "operation" : "last_will",
                        "value": "error"}
client.will_set("house/light", json.dumps(last_will_data), qos=2)   

client.connect(broker)
client.loop_start()    
client.subscribe("house/light")
print("Sender aktiviert")


basic_light = 10

while True:
    for sensor_index in range (0, sensor_count):
        basic_light = random.randint(1, 100)

        sensor_data = {"uuid": uuid_list[sensor_index],
                        "type": "light",
                        "operation" : "update",
                        "value": basic_light}
        client.publish("house/light", json.dumps(sensor_data), qos=1)
        print(sensor_data)

    time.sleep(5)