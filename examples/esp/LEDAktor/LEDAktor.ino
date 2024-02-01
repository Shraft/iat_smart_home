#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> //Arduino JSON Library

/***
  This application is still under development and functionality is not guaranteed.
  The goal of this application is to receive RGB values via MQTT from a subscibed topic and then control a lightsource like an LED.
***/

/*** Functionality Configuration ***/
#define LAST_WILL
#define SUBSCRIBE_LED

/*** configure LED ***/
#define TOPIC_LED "house/light"
#define PIN_LED_R D5
#define PIN_LED_G D6
#define PIN_LED_B D7

/*** Miscelaneous Configuration ***/
#define SENSOR_UUID 55555

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


StaticJsonDocument<200> tempJson;  //reserve 200 Byte for the JSON

/** instanciate Wifi, MQTT & DHT **/
WiFiClient client;
PubSubClient mqttClient(client);

/*** Establishes WLAN and MQTT connection ***/
void connect() {
  // loop until WLAN connected
  while (!client.connected()){

    // try mqtt connection
    Serial.println("Versuche MQTT Verbindungsaufbau!");
    if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("MQTT verbunden!");
      #if defined(SUBSCRIBE_LED)
        mqttClient.subscribe(TOPIC_LED,1);
      #endif
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

/*** Callback function, is called when receiving subscribed data ***/
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
        Serial.println("Received RGB Values for this unit");
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
        Serial.println("RGB Values not for this unit");
      }
    }
  #endif
}


void setup() {
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
    tempJson["type"] = "led";
    tempJson["operation"] = "last_will";
    tempJson["value"] = "error";
    serializeJson(tempJson, message);
    Serial.println(message);
    sendMessage(message);
  #endif

  #if defined(SUBSCRIBE_LED)
    pinMode(PIN_LED_R, OUTPUT);
    pinMode(PIN_LED_G, OUTPUT);
    pinMode(PIN_LED_B, OUTPUT);
    mqttClient.setCallback(callback);
  #endif

}

void loop() {
   // not needed yet

}
