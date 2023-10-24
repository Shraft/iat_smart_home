import time
import paho.mqtt.client as mqtt


broker = "192.168.158.11"

client = mqtt.Client("sender")

client.connect(broker)

client.subscribe("house/main")

print("Sender aktiviert")

while True:
    client.publish("house/main", "Sensor 1 ist online")
    print("Nachricht wurde gesendet")
    time.sleep(3)
