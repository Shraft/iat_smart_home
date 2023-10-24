import time
import paho.mqtt.client as mqtt


broker = "localhost"

client = mqtt.Client("sender")

client.connect(broker)

client.subscribe("house/main")

print("Sender aktiviert")

while True:
    client.publish("house/main", "Sensor 1 ist online")
    print("Nachricht wurde gesendet")
    time.sleep(3)
