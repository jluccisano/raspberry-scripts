# Start Virtualenv


virtualenv -p /usr/bin/python2.7 ~/workspace/venv2.7/
source ~/workspace/venv2.7/bin/activate

# Install Flask

pip install Flask

# Run sprinkler server

FLASK_APP=server.py flask run --host=0.0.0.0 --port=8515
