## Measure Temperature
The goal of this example is to measure temperature and humidity with an DHT11 Sensor on a NodeMCUv3 esp board.
requirements:
* Arduino IDE
* NodeMCUv3 Board
* DHT11 Temperature/Humidity Sensor

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
  <img src="https://github.com/Shraft/iat_smart_home/assets/67481239/2124f4e0-9951-40dc-8fb4-0dc995ef6b8c" alt="Sublime's custom image"/>
</p>
4. Adafruit DHT sensor library installieren
<p align="left">
  <img src="https://github.com/Shraft/iat_smart_home/assets/67481239/5c9f9dbb-167f-4d51-ae9c-1897ce60641b" alt="Sublime's custom image"/>
</p>

### NodeMCUv3 Setup
Connect the DHT11 with 3.3V, Ground and the data pin to Pin "D0" of the NodeMCU
<p align="left">
  <img src="https://preview.redd.it/kiygdnluwar81.jpg?width=500&format=pjpg&auto=webp&s=eb7f327f0d370fbcb57835b16c270bb6a19411ef" alt="Sublime's custom image" width="400"/>
  <img src="https://github.com/Shraft/iat_smart_home/assets/67481239/fad544d6-1ef2-48bd-9fff-fdac136b8bf0" alt="Sublime's custom image" width="400"/>
</p>



