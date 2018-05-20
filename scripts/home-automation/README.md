# Start Virtualenv

```bash
virtualenv -p /usr/bin/python2.7 ~/workspace/venv2.7/
```

```bash
source ~/workspace/venv2.7/bin/activate
```

# Install Flask
```bash
pip install Flask
```
```bash
pip install RPi.GPIO
```
or for development mode.
https://github.com/willbuckner/rpi-gpio-development-mock

```bash
pip install tqdm    
```

sudo cp ~/workspace/raspberry-scripts/scripts/home-automation home-automation -r


sudo ln -s ~/workspace/raspberry-scripts/scripts/home-automation /opt/home-automation

Create server.conf file

sudo vim server.conf


# Run local sprinkler server

```bash
FLASK_APP=server.py flask run --host=0.0.0.0 --port=8515
```
or 

```bash
python server.py
```


# Create  a service

```bash
sudo vim /lib/systemd/system/home-automation.service
```
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/sect-managing_services_with_systemd-unit_files

```text
[Unit]
Description=Home Automation Server
After=multi-user.target

[Service]
ExecStart=/usr/bin/python /opt/home-automation/server.py
Type=simple
Restart=on-abort
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
https://jluccisano.github.io/linux/create-service/
```

```bash
sudo systemctl enable home-automation.service
```

```bash
sudo chmod u+x server.py
```

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl start home-automation.service
```

```bash
sudo systemctl status home-automation.service
```

```bash
sudo systemctl stop home-automation.service
```

```bash
tail -f /var/log/syslog
```

```bash
● home-automation.service - Home Automation Server
   Loaded: loaded (/lib/systemd/system/home-automation.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2018-05-18 12:31:25 UTC; 60ms ago
 Main PID: 13583 (python)
   Memory: 1.7M
      CPU: 51ms
   CGroup: /system.slice/home-automation.service
           └─13583 /usr/bin/python /opt/home-automation/server.py

May 18 12:31:25 raspberrypi systemd[1]: Started Home Automation Server.
```

# Tests

# Sprinkler API

```bash
curl -X GET -u user:passwd "http://192.168.0.13:8515/sprinkler/zones"
```

```bash
curl -X POST -u user:passwd "http://192.168.0.13:8515/sprinkler/zones?format=lite"
```

```bash
curl -X POST -u user:passwd "http://192.168.0.13:8515/sprinkler/zones/1?state=0"
```

```bash
curl -X POST -u user:passwd "http://192.168.0.13:8515/sprinkler/zones/1/toggle"
```


```bash
curl -X POST -u user:passwd "http://192.168.0.13:8515/sprinkler/zones?state=0"
```

```bash
curl -X POST -u user:passwd "http://192.168.0.13:8515/sprinkler/reset"
```

```bash
curl -X POST \
     --header "Content-Type: application/json" \
     -u user:passwd \
     -d '[{
         	"duration": "5",
         	"zone": "1",
         	"description": "Zone A"
         },
         {
         	"duration": "5",
         	"zone": "2",
         	"description": "Zone B"
         },
         {
         	"duration": "5",
         	"zone": "3",
         	"description": "Zone C"
         }]' \
     "http://192.168.0.13:8515/sprinkler/scenario"
```

or with form param (useful with curler application which don't manage json body)

```bash
curl -X POST \
     -u user:passwd \
     -F 'data=[{"duration": "10", "zone": "1", "description": "Zone A" },{"duration": "10", "zone": "2", "description": "Zone B" }]' \
     "http://192.168.0.13:8515/sprinkler/scenario"
```

# Camera API

```bash
curl -X GET -u user:passwd "http://localhost:8515/cameras?name=Camera%20Salon"
```

```bash
curl -X POST -u user:passwd "http://localhost:8515/cameras/13/enable"
```

```bash
curl -X POST -u user:passwd "http://localhost:8515/cameras/13/disable"
```
