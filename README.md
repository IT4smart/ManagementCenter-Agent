# Management Agent
Der Agent ist in Python geschrieben und ist fuer die Kommunikation mit der Verwaltungskonsole zustaendig.

## Build dependencies
* dh-systemd
* python-virtualenv
* dh-virtualenv
* crossbuild-essential-armhf

## Paketbau
Um Pakete für eine spezielle Architektur zu bauen muss das folgende angegeben werden `dpkg-buildpackage -aarmhf -us -uc`.