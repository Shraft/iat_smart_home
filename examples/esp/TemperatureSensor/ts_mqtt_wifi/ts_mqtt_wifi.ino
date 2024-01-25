#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <ArduinoJson.h> //Arduino JSON Library

//DHT sensor benutzen
#define DHT_PIN 4
#define DHT_TYPE DHT11 //Pins definieren (DHT11 oder DHT22)
#define DHT_GET_TEMP
// #define DHT_GET_HUMIDITY
// #define DHT_GET_HEAT_INDEX

//Wlan Name und Password Setzen
const char *WIFI_SSID = "smart_home_wifi";
const char *WIFI_PASSWORD = "smarthome";

//MQTT Parameter setzen
const char *MQTT_HOST = "192.168.0.112";
const int MQTT_PORT = 1883;
const char *MQTT_CLIENT_ID = "ESPts1";
const char *MQTT_PASSWORD = "";
const char *MQTT_USER = "ESPts1";
const char *TOPIC = "house/main";

//Wifi, MQTT & TS instanziieren
WiFiClient client;
PubSubClient mqttClient(client);
DHT dht(DHT_PIN, DHT_TYPE);

int last_read = 0;     // gibt an, wann als letzes vom TS gelesen wurde
StaticJsonDocument<200> tempJson;  //Json um die Daten den Temperatursensors zu übermitteln 


// die connect funktion baut die Wlan und MQTT Verbindung auf
void connect() {
  // Schleife endet erst, wenn wifi verbunden
  while (!client.connected()){

    // versuche mqtt Verbindungsaufbau
    Serial.println("Versuche MQTT Verbindungsaufbau!");
    if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("MQTT verbunden!");
      mqttClient.subscribe(TOPIC,1);  // wenn verbunden, subscripe Topic
    } else {
      Serial.println("MQTT fehlgeschlagen, versuche es erneut!");    
      delay(5000);
    }
  }
}

void sendMessage(String message){
  // forme den String in ein array of char um
      int n = message.length();
      char char_array[n + 1];
      message.toCharArray(char_array, n+1);

      // wenn Verbindung abgebrochen, baue eine neue auf
      if (!client.connected()){
        connect();
        }
      mqttClient.publish(TOPIC, char_array);  // versende die Nachricht mit MQTT
}


// Setup vornehmen
void setup() {
  //serielle Verbindung starten
  Serial.begin(115200);

  // starte wifi Verbindung
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Verbindungsaufbau zum Wifi ");
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());

  // einstellungen für automatischen wifi reconnect
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);

  // initialisiere MQTT
  mqttClient.setServer(MQTT_HOST,MQTT_PORT);
  connect();

  // initialisiere DHT
  #if defined(DHT_GET_TEMP) || defined(DHT_GET_HUMIDITY) || defined(DHT_GET_HEAT_INDEX)
    dht.begin();
  #endif
}


// loop Teil wird immer wieder ausgefuehrt
void loop() {

  #if defined(DHT_GET_TEMP) || defined(DHT_GET_HUMIDITY) || defined(DHT_GET_HEAT_INDEX)
    // wenn die letzte Sensorauswertung länger als 2 Sekunden her ist, lese erneut
    if (last_read > 2000){
      float h = dht.readHumidity();                       // Luftfeuchtigkeit
      float t = dht.readTemperature();                    // Temperatur
      float hi = dht.computeHeatIndex(t, h, false);       // Hitzeindex

      // pruefe ob Daten fehlerhaft sind
      if (isnan(h) || isnan(t)){
        Serial.println("Lesefehler vom Sensor");
        last_read = 0;
        return;
      }

      // setze die zu versendende Temperatur Nachricht zusammen
      # ifdef DHT_GET_TEMP
        String message = "";
        tempJson["uuid"] = 44444;
        tempJson["type"] = "temp";
        tempJson["operation"] = "update";
        tempJson["value"] = t;
        serializeJson(tempJson, message);
        Serial.println(message);
        sendMessage(message);
      #endif
      // sende feuchtigkeit
      # ifdef DHT_GET_HUMIDITY
        String message = "";
        tempJson["uuid"] = 44444;
        tempJson["type"] = "hum";
        tempJson["operation"] = "update";
        tempJson["value"] = h;
        serializeJson(tempJson, message);
        Serial.println(message);
        sendMessage(message);
      #endif
      //sende heat index
      # ifdef DHT_GET_HEAT_INDEX
        String message = "";
        tempJson["uuid"] = 44444;
        tempJson["type"] = "hi";
        tempJson["operation"] = "update";
        tempJson["value"] = hi;
        serializeJson(tempJson, message);
        Serial.println(message);
        sendMessage(message);
      #endif

      // setze den letzten Lesezeitpunkt auf 0 zurück
      last_read = 0;
    #endif
  }

  // warte, bis wieder gelesen werden muss
  delay(100);
  last_read += 100;
}
