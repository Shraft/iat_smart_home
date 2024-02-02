# smart home system für iat

## Setup Anleitung

Wichtig:
1. Die folgenden Schritte wurden unter Ubuntu getestet
2. Das Terminal muss sich für die folgenden befehle immer im
verzeichnis des Projektes befinden, also nicht in einem unterverzeichnis
/path/to/iat_smart_home directory

### 1. docker-compose ausführen

#### install docker and docker-compose

```
sudo curl https://get.docker.com | bash
sudo apt install docker-compose
```

#### Die Zentrale, den Broker und die Datenbank starten
##### Container bauen
```
docker-compose -f docker/docker-compose.yml build
```

##### Container starten

```
docker-compose -f docker/docker-compose.yml up
```

zum beenden dann einfach STRG+C drücken

### 2. Die Simulationsprogramme starten
### virtualenv
##### about virtualenv

A virtualenv in Python is a self-contained and isolated environment that allows developers to manage and install dependencies for a specific project without affecting the system-wide Python installation.

##### installieren
```
apt install python3-pip
apt install python3-virtualenv
```

##### virtuelle umgebung anlegen
```
virtualenv .venv
```

##### requirements installieren
```
pip3 -r requiments.txt install
```
###### activate virtualenv
```
source .venv/bin/activate
```

##### Temperatursensor starten
```
python3 tools/temp_sensor.py
```

##### Lichtsensor starten
```
python3 tools/ligt_sensor.py
```

##### RFID-SImulator starten
```
python3 tools/rfid_simulator.py
```

Beenden jeweils wieder mit STRG + C

### 3. Webseite aufrufen

diese ist unter http://localhost:8080 zu erreichen
