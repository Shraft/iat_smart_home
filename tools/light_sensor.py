import time
import paho.mqtt.client as mqtt
import json
import random

uuid = random.randint(100000, 999999)
sensor_count = 0


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
    print(data)
    
    if "addressee" in data:
        if data["addressee"] == "slave":
            if data["uuid"] == uuid:
                print_rgb_color(data["r"],data["g"], data["b"], f"Sensor-{data['uuid']}")
    

counter = 0
send_delay = 2
recon_time = 30
while True:
    counter += 1

    if counter == 1:
        broker = "localhost"
        client = mqtt.Client(f"light_sender-{uuid}")

        # Last will implementation
        last_will_data = {"uuid": uuid,
                        "type": "light",
                        "operation" : "last_will",
                        "value": "error"}
        client.will_set("house/light", json.dumps(last_will_data), qos=2)   

        client.on_message = mqtt_on_message_callback  
        client.connect(broker)
        client.loop_start()   
        client.subscribe("house/#")
        print(f"Sender aktiviert mit UUID {uuid}")
    elif counter == int(recon_time/send_delay):
        client.disconnect()
        print("disconnect")
        counter = 0
        continue


    basic_light = random.randint(1, 100)

    sensor_data = {"uuid": uuid,
                    "type": "light",
                    "operation" : "update",
                    "value": basic_light}
    client.publish("house/light", json.dumps(sensor_data), qos=1)
    #print(sensor_data)

    time.sleep(send_delay)