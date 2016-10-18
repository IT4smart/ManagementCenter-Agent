# Management Agent
Der Agent ist in Python geschrieben und ist fuer die Kommunikation mit der Verwaltungskonsole zustaendig.

## Systemd Service
1. `sudo nano /lib/systemd/system/IT4S_Agent.service`
2. `[Unit]
    Description=IT4S Agent
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python /home/test/Management_Agent/Run.py

    [Install]
    WantedBy=multi-user.target`
3. `sudo chmod 644 /lib/systemd/system/ÌT4S_Agent.service`
4. `sudo systemctl daemon-reload`
5. `sudo systemctl enable IT4S_Agent.service`
6. `sudo reboot`