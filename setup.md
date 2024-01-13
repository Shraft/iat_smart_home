## smart home system for iat

### setting up project

#### use virtualenv
##### installieren
```
apt install python3-pip
apt install python3-virtualenv
```

##### anlegen & activieren
```
virtualenv .venv
source .venv/bin/activate
```

##### deaktivieren
```
deactivate
```

### files and directories

#### /docker 
contains all docker files

#### /src/flask-server 
app for the webserver providing all pages

#### /src/com-server 
app for both websocket to frondend and mqtt connection

### other informations
proof of concept only!
