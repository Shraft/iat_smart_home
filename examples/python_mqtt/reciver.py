import time
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    print("EMPFANGEN: " + str(message.payload.decode("utf-8")))

broker = "localhost"

client = mqtt.Client("receiver")

client.connect(broker)
client.on_message = on_message

client.subscribe("house/#")
client.loop_start()

print("Empfänger aktiviert")

time.sleep(60)

client.loop_stop()
client.disconnect()
