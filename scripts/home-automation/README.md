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

# Create server.conf file


# Run local sprinkler server

```bash
FLASK_APP=server.py flask run --host=0.0.0.0 --port=8515
```
or 

```bash
python server.py
```

# Tests

# Sprinkler API

```bash
curl -X GET -u user:passwd "http://192.168.0.13:8515/sprinkler/zones"
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
