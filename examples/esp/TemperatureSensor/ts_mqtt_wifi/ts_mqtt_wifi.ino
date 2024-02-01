#include "DHT.h" // Temperature Sensor Library
#include <ESP8266WiFi.h>  //Library for interacting with the ESP Board
#include <PubSubClient.h> // MQTT Library
#include <ArduinoJson.h> //Arduino JSON Library

/***
  This Programm connects via MQTT-TCP to a broker and transmits optionally temperature/ humidity / heat index
  The functionality can be configured by commenting the defines accordingly
  This application is intendet to work with a DHT 11 or 22 Temperature Sensor and a Nodemcu V1 board, that features an esp8266 wlan microcontroller.
  For simplicity the sensor/actors are split into different applications.
***/

/*** Functionality Configuration ***/
#define LAST_WILL
#define DHT_GET_TEMP  //DHT sensor benutzen
  // #define DHT_GET_HUMIDITY
  // #define DHT_GET_HEAT_INDEX

/*** Configure DHT ***/
#define DHT_PIN D2  // Pin where the used DHT signal pin is
#define DHT_TYPE DHT11 //Define DHT model (DHT11 oder DHT22)
#define DHT_READ_INTERVALL_MS 2000

/*** Miscelaneous Configuration ***/
#define SENSOR_UUID 44444 //Unique Identifier

/*** Set WLAN Name and Password ***/
const char *WIFI_SSID = "Axayacatl";//"smart_home_wifi";
const char *WIFI_PASSWORD = "47597001200484786023";//"smarthome";

/*** set MQTT Parameter ***/
const char *MQTT_HOST = "192.168.178.40";//"192.168.0.112";
const int MQTT_PORT = 1883;
const char *MQTT_CLIENT_ID = "ESPts1";
const char *MQTT_PASSWORD = "";
const char *MQTT_USER = "ESPts1";
const char *TOPIC = "house/main";

/** instanciate Wifi, MQTT & DHT **/
WiFiClient client;
PubSubClient mqttClient(client);
DHT dht(DHT_PIN, DHT_TYPE);

int last_read = 0;     // time from last read from dht
StaticJsonDocument<200> tempJson;  //reserve 200 Byte for the JSON


/*** Establishes WLAN and MQTT connection ***/
void connect() {
  // loop until WLAN connected
  while (!client.connected()){

    // try mqtt connection
    Serial.println("Versuche MQTT Verbindungsaufbau!");
    if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("MQTT verbunden!");
    } else {
      Serial.println("MQTT fehlgeschlagen, versuche es erneut!");    
      delay(5000); // retry in 5 seconds
    }
  }
}


/*** Helper function for publishing data ***/
void sendMessage(String message){
  // string to char array
  char char_array[message.length() + 1];
  message.toCharArray(char_array, message.length()+1);

  // when connection is lost, create connection
  if (!client.connected()) connect();
  mqttClient.publish(TOPIC, char_array);  // send message
}


/*** initialize controller ***/
void setup() {
  Serial.begin(115200); // create serial connection for debugging / status information

  /** create and configure wifi connection***/
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Verbindungsaufbau zum Wifi ");
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.print("Assigned IP adress is: ");
  Serial.println(WiFi.localIP());

  // setting for automatic wifi reconnect
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);

  // initialize MQTT
  mqttClient.setServer(MQTT_HOST,MQTT_PORT);
  connect(); //establish connection
  
  /*** If LAST_WILL ist defined, then the last will message is send to the broker***/
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

  // iinitialize DHT
  #if defined(DHT_GET_TEMP) || defined(DHT_GET_HUMIDITY) || defined(DHT_GET_HEAT_INDEX)
    dht.begin();
  #endif
}


/*** main loop ***/
void loop() {
  /*** when data from the dht sensor is needed ***/
  #if defined(DHT_GET_TEMP) || defined(DHT_GET_HUMIDITY) || defined(DHT_GET_HEAT_INDEX)
    // if last read from sensor is older than 2 seconds, then read again
    if (last_read > DHT_READ_INTERVALL_MS){
      float h = dht.readHumidity();                       // Humidity
      float t = dht.readTemperature();                    // Temperature
      float hi = dht.computeHeatIndex(t, h, false);       // Heatindex

      // check for faulty data
      if (isnan(h) || isnan(t)){
        Serial.println("Lesefehler vom Sensor");
        last_read = 0;
        return;
      }

      // publish temperature data
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
      // publish humidity data
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
      //publish heat index
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

      // reset last read time
      last_read = 0;
    #endif
  }

  // wait for next read
  delay(100); // could be replaced by 100ms deep sleep
  last_read += 100;
}
