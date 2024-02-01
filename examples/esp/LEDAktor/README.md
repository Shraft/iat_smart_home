## Control LED WIP

The goal of this example is to subscribe to a mqtt topic and set the led color with the values received form said topic. 

### Requirements:

* Arduino IDE
* NodeMCUv3 Board
* LED

### ARDUINO IDE

1. Install board suport package by:
   Open Arduino IDE, then File->Preferences->additional board manager urls => add the following lines

```
http://arduino.esp8266.com/stable/package_esp8266com_index.json
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

2. Now got to Tools > Board > Boards Manager => search for esp8366 and install the package

<p align="left">
  <img src="https://github.com/Shraft/iat_smart_home/assets/67481239/79312e1c-da02-47aa-99a1-8adc181180df" alt="Sublime's custom image"/>
</p>

3. Select Board => NodeMCU 1.0

<p align="left">
  <img src="https://github.com/Shraft/iat_smart_home/assets/67481239/2124f4e0-9951-40dc-8fb4-0dc995ef6b8c" alt="Sublime's custom image" width="400"/>
</p>


5. Now install the following librarys the same way
   - "Arduino JSON Library"
   - PubSubClient

### NodeMCUv3 Setup

Connect the Pins of the LED to a any gpio of the nodemcu.


### Configuring the Sensor

By commenting and uncommenting the following lines can topics be enabled and disabled

```
/*** Functionality Configuration ***/
#define LAST_WILL
#define SUBSCRIBE_LED

/*** configure LED ***/
#define TOPIC_LED "house/light"
#define PIN_LED_R D5
#define PIN_LED_G D6
#define PIN_LED_B D7
```

Check that the right pin is selected and the wifi credentials are correct and then compile and upload your programm to the esp

