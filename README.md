# Belegarbeit
Entwicklung einer Demoanwendung für die Lehre unter verwendung von MQTT

## Motivation - Warum sollte man sich mit diesem Thema auseinandersetzen
1. **IoT-Essential:**
   MQTT ist ein grundlegendes Protokoll im Internet der Dinge (IoT) und ermöglicht die effiziente Kommunikation zwischen vernetzten Geräten. Wer sich mit MQTT beschäftigt, taucht in die Welt der IoT-Technologien ein.

2. **Effiziente Datenübertragung:**
   MQTT zeichnet sich durch einen geringen Overhead aus, was zu einer effizienten Datenübertragung führt. Dies ist besonders wichtig in Umgebungen mit begrenzten Ressourcen und Bandbreite.

3. **Skalierbarkeit für Projekte aller Größen:**
   Egal, ob Sie ein kleines Heimautomatisierungsprojekt oder ein groß angelegtes Industrie-Deployment planen, MQTT bietet Skalierbarkeit und Flexibilität für Projekte aller Größenordnungen.

4. **Einfache Implementierung:**
   MQTT ist einfach zu implementieren, was den Einstieg erleichtert, und es gibt viele Bibliotheken für verschiedene Programmiersprachen, was die Entwicklungszeit verkürzt. Dies ermöglicht Entwicklern, schnell Prototypen zu erstellen und ihre Ideen umzusetzen.

5. **Vielseitige Anwendungsbereiche:**
   MQTT ist nicht nur auf IoT beschränkt. Es findet Anwendung in verschiedenen Szenarien wie Echtzeit-Messaging, Home Automation, Logistik und mehr. Die Vielseitigkeit des Protokolls macht es zu einer wertvollen Fähigkeit.

6. **Zuverlässige Kommunikation:**
   Durch die Möglichkeit, den Quality of Service (QoS) Level anzupassen, bietet MQTT eine zuverlässige Kommunikation, selbst in instabilen Netzwerken. Das ist besonders wichtig in Umgebungen, in denen eine zuverlässige Datenübertragung entscheidend ist.

Aufgrund der genannten Eigenschaft gewinnt das MQTT-Protokoll zunehmend an Bedeutung. Aus diesem Grund ist es von großem Nutzen, sich einmal genauer mit dieser Technologie zu beschäftigen.

## Anforderungen
- MQTT: Quality of Service Level kurz QOS
   - ermöglichen die Zustellparameter einzelner Nachrichten zu individualisieren
   - 0..höchstens einmal, 1..mindestens einmal, 2..genau einmal
- MQTT: Letzer Wille
   - wird von MQTT sender beim Verbindungsaufbau zum Broker definiert
   - Broker führt letzen Willen bei Verbindungsabbruch des Senders aus
- Security
   - alle Nachrichten werden unverschlüsselt versendet
   - das Projekt sieht keine Sicherheitsmechanismen vor
- Software Simmulierte Sensoren
   - midestens 3 in Software simmulierte Sensoren
   - Generieren Zufallswerte und versenden diese via MQTT
- Physische Sensoren
   - ein Sensor soll als physische Komponente realisiert werden 
- Skalierbarkeit / Modulariät
   - das System soll mit beliebig vielen Sensoren erweiterbar sein
- Geringer Overhead (Pakete einfach)
   - Die Kommunizierten Nachrichten beinhalten nur relevante Informationen
- Visualisierbakeit / grafische Aufbereitung
   - Die Werte der Sensoren soll über eine Web Oberfläche einsehbar sein
   - Aktoren sollen ihre Instruktionen ebenfalls über dieses Interface erhalten
- Nutzerinteraktion
   - Der Nutzer soll in der lage sein, selbst Steuergrößen anzugeben

## Entwurf
- skizzen
- hinführen zum endergebnis

## Werkzeuge
- Arduino Libraries
- Python Libraries
   - PahoMQTT
      - ermöglicht in MQTT Nachrichten zu senden und zu empfangen
   - SQLAlchemy
      - ermöglicht das senden von SQL Anfragen an eine Datenbank
      - notwendig zum speichern und abrufen von Sensorwerten
   - Flask
      - Framework um Python als Webserver zu nutzen
      - Stellt HTML Seiten bereit
      - Dient als Kommunikationsparter für eine Websocket Verbindung mit dem Frontend
   - Plotly
      - kann aus Datenstrukturen Diagramme erstellen und als HTML Seite exportieren

## Implementierung
- Code Schnipsel

## Diskussion der Ergebnisse - Probleme
- Security muss erweitert werden
- Verfügbarkeit - SPoF Broker

## Anhang
- Docker zeug
