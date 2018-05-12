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
```bash
pip install tqdm
```

# Run sprinkler server

```bash
FLASK_APP=server.py flask run --host=0.0.0.0 --port=8515
```

# Tests

```bash
curl -X GET http://192.168.0.13:8515/sprinkler/zones
```

```bash
curl -X POST http://192.168.0.13:8515/sprinkler/zone/1?state=0
```

```bash
curl -X POST http://192.168.0.13:8515/sprinkler/zone/1/toggle
```

```bash
curl -X POST http://192.168.0.13:8515/sprinkler/zones?state=0
```

```bash
curl -X POST http://192.168.0.13:8515/sprinkler/reset
```

