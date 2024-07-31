# Masterarbeit 

## Description
Eine Webanwendung wurde entwickelt, die einen Annotationsprozess implementiert für die Erstellung von Annotation für Textdaten. Die Anwendung setzt sich aus einer Angular-Frontend und einer Django-Backend Komponente zusammen. Als Datenbank wurde SQLite gewählt. Die Anwendung wurde über einen VPS mithilfe von Docker veröffentlicht.
Die Anwendung ist über den Link https://everythinkatonce.de/ erreichbar.

## Installation
Die Anwendung kann local über Docker gestartet werden. Dazu muss zunächst dieses Projekt geclont werden.
Die Anwendung besteht aus zwei Docker Containern.

Der Container für das Frontend wird über den Befehl 
```docker build -t <repo>:<tag> .``` 
erstellt

Der Container für das Backend wird über den Befehl 
```docker build -t <repo>:<tag> --build-arg DJANGO_SUPERUSER_USERNAME= --build-arg DJANGO_SUPERUSER_EMAIL= --build-arg DJANGO_SUPERUSER_PASSWORD= .``` 
erstellt

Zu beachten gilt hierbei, dass die Einstellungen des Backends-Projektes ein SSL-Zertifikat vorraussetzen. 
Zu einer lokalen Nutzung müssen eventuelle Anpassungen in der settings.py-Datei im Backend und im Frontend in der nginx.conf und environment-Datei gemacht werden.

## Support
Bei Problemen kann ein Issue aufgemacht werden oder eine Email an marie.braun@hhu.de geschickt werden.