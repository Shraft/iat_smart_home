#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <PubSubClient.h>
#include "DHT.h"
#include <ArduinoJson.h> //Arduino JSON Library
#include <iostream>

//DHT sensor benutzen
#define DHT_PIN D2
#define DHT_TYPE DHT11 //Pins definieren (DHT11 oder DHT22)
#define DHT_GET_TEMP
#define SUBSCRIBE_LED
#define PIN_LED_R D5
#define PIN_LED_G D6
#define PIN_LED_B D7
#define TOPIC_LED "house/light"
// #define DHT_GET_HUMIDITY
// #define DHT_GET_HEAT_INDEX
#define LAST_WILL

#define SENSOR_UUID 44444

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

//Wifi, MQTT & DHT instanzieren
WiFiClient client;
PubSubClient mqttClient(client);
DHT dht(DHT_PIN, DHT_TYPE);

int last_read = 0;     // gibt an, wann als letzes vom TS gelesen wurde
StaticJsonDocument<200> tempJson;  //Json um die Daten den Temperatursensors zu übermitteln (200Byte ram reserviert)


// die connect funktion baut die Wlan und MQTT Verbindung auf
void connect() {
  // Schleife endet erst, wenn wifi verbunden
  while (!client.connected()){

    // versuche mqtt Verbindungsaufbau
    Serial.println("Versuche MQTT Verbindungsaufbau!");
    if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("MQTT verbunden!");
      //mqttClient.subscribe(TOPIC,1);  // wenn verbunden, subscripe Topic
      #if defined(SUBSCRIBE_LED)
        mqttClient.subscribe(TOPIC_LED,1);
      #endif
    } else {
      Serial.println("MQTT fehlgeschlagen, versuche es erneut!");    
      delay(5000);
    }
  }
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off". 
  // Changes the output state according to the message
  #if defined(SUBSCRIBE_LED)
    if (String(topic) == TOPIC_LED) {
      Serial.print("Changing led color ");
      //convert byte array to char array
      using byte = unsigned char;
      // Allocate a char array with one extra space for the null terminator
      char json[length + 1];
      // Copy bytes from message to json
      for (unsigned int i = 0; i < length; ++i) {
          json[i] = static_cast<char>(message[i]);
      }
      // Null-terminate the char array
      json[length] = '\0';
      //extract json data
      JsonDocument doc_sub;
      deserializeJson(doc_sub, json);
      //check if data is for this device
      if (doc_sub["uuid"] == SENSOR_UUID){
        Serial.println("Received RGV Values for this unit");
        int R = doc_sub["r"];
        int G = doc_sub["g"];
        int B = doc_sub["b"];
        if (R > 255) R = 255;
        if (G > 255) G = 255;
        if (B > 255) B = 255; 
        analogWrite(PIN_LED_R, R);
        analogWrite(PIN_LED_G, G);
        analogWrite(PIN_LED_B, B);
      }else{
        Serial.println("RGV Values not for this unit");
      }
    }
  #endif
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
  //set callback for subscibed topics
mqttClient.setCallback(callback);
  #if defined(SUBSCRIBE_LED)
    pinMode(PIN_LED_R, OUTPUT);
    pinMode(PIN_LED_G, OUTPUT);
    pinMode(PIN_LED_B, OUTPUT);
  #endif

  // initialisiere MQTT
  mqttClient.setServer(MQTT_HOST,MQTT_PORT);
  connect();
  //last will
  #if defined(LAST_WILL)
    String message = "";
    tempJson["uuid"] = SENSOR_UUID;
    tempJson["type"] = "temp";
    tempJson["operation"] = "last_will";
    tempJson["value"] = "error";
    serializeJson(tempJson, message);
    Serial.println(message);
    sendMessage(message);
  #endif

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
        tempJson["uuid"] = SENSOR_UUID;
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
        tempJson["uuid"] = SENSOR_UUID;
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
        tempJson["uuid"] = SENSOR_UUID;
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
