# Start Virtualenv


virtualenv -p /usr/bin/python2.7 ~/workspace/venv2.7/
source ~/workspace/venv2.7/bin/activate

# Install Flask

pip install Flask
pip install RPi.GPIO
pip install tqdm

# Run sprinkler server

FLASK_APP=server.py flask run --host=0.0.0.0 --port=8515


# Tests

curl -X GET http://192.168.0.13:8515/sprinkler/zones


curl -X POST http://192.168.0.13:8515/sprinkler/zone/1

