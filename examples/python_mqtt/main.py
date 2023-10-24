import time
import paho.mqtt.client as mqtt


# definiere eine Funktion, die aufgerufen werden soll, sobald eine Nachricht empfangen wurde
def on_message(client, userdata, message):
    print("Nachricht erhalten: " + str(message.payload.decode("utf-8")))


def main():
    broker_address = "192.168.158.11"       # setze broker ip

    client = mqtt.Client("master")          # instanziiere mqtt client
    client.on_message = on_message          # gebe die Funktion an fuer Eingehende Nachrichten

    client.connect(broker_address)          # stelle die Verbindung zu Broker her
    client.loop_start()                     # starte die loop, welche dafuer sorgt,
                                            # das permanent nach Nachrichten geschaut wird

    client.subscribe("house/main")          # subscribe der topic

    client.publish("house/main", "Die Zentrale ist jetzt online")   # sende eine Nachricht

    time.sleep(3)                           # verzoegere

    client.loop_stop()                      # stoppe die loop
    client.disconnect()                     # breche die Verbindung zum server ab



# wenn die Datei main.py heist, dann rufe die main() Funktion auf
if __name__ == '__main__':
    main()
