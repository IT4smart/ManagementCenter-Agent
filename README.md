# Management Agent
Der Agent ist in Python geschrieben und ist fuer die Kommunikation mit der Verwaltungskonsole zustaendig.


## Build dependencies
* dh-systemd
* python-virtualenv
* dh-virtualenv
* python2.7-dev
* python2.7


## Release
Die Versionierung des Management-Agent folgt der "Semantic Versioning" (http://semver.org/).

Um ein Release zu erstellen wird in der Datei 'setup.py' die Versionsnummer im Feld 'Version' erhöht. Daraufhin wird ein 'Commit' erstellt mit dem Text 'bump to <Version>'.
Dieser 'Commit' ist dann zu pushen. Im Anschluss muss der Hash des 'Commits' herausgefunden werden, denn wir hängen ein Tag an dieses 'Commit'.

Um das ganze zu taggen verwenden wir den folgenden Befehl ``git tag <version> <commit hash>``. Zum Schluss pushen wir diesen noch mit dem Befehl ``git push origin <version>``.


## Paketbau
Aus den quellen kann mithilfe eines Chroot für jede beliebige Architektur ein Paket gebaut werden. Dazu muss das GIT-Repository 'BuildSystemRPi' heruntergeladen werden. 
Hier ist in den Ordner 'packages/management-agent' zu wechseln.

Dort ist dann in das Terminal der folgende Befehl einzugeben ``make <architecture>``. Zur Zeit stehen die folgenden Architekturen zur Verfügung:
* ARMHF (ARM HardFloat)
* AMD64 (64-bit Architektur, kein ARM 64-bit)
* i686 (32-bit Architektur)

Wenn die Chroot - Umgebung erfolgreich geladen wurde, muss ins Terminal der folgende Befehl eingegeben werden ``export DH_VIRTUALENV_INSTALL_ROOT=/opt/IT4S``.

Im Anschluss daran wird in das Verzeichnis '/tmp' gewechselt. Dort muss die virtuelle Umgebung für Python aktiviert werden. Dies geschiet durch den Befehl ``source virt-example/bin/activate``.

Nun wechseln wir in das Verzeichnis in dem die Quellen liegen. Das Verzeichnis heißt 'Verwaltungskonsole-Agent'. Zunächst wechseln wir zum "commit" des aktuellsten Tags ``git checkout $(git describe --tags `git rev-list --tags --max-count=1`)``.

Anschließend wird immer das aktuelle Changelog generiert mit dem Befehl ``./changelog > debian/changelog``. 
Im Anschluss wird dann der Befehl ``dpkg-buildpackage -us -uc`` eingegeben und ausgeführt um das Debianpaket zu erstellen.