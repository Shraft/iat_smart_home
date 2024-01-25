import time
import paho.mqtt.client as mqtt


broker = "localhost"

client = mqtt.Client("sender")

client.will_set("house/main", "Verbindung zum Sender unterbrochen", 2)

client.connect(broker)


print("Sender aktiviert")

while True:
    client.publish("house/main", "Sensor 1: Daten ...", qos=1)
    print("Nachricht wurde gesendet")
    time.sleep(2)
