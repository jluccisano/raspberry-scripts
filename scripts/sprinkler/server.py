from zone_control import ZoneControl
from flask import Flask
from flask import request
import json

app = Flask(__name__)

data = {}
with open('data.json') as data_file:
    data = json.load(data_file)

zone_control = ZoneControl()

# POST /sprinkler/zone/1?state=1
@app.route("/sprinkler/zone/<zone>")
def set_zone(zone):
    state = request.args.get('state')
    return "Hello World!" + state


# GET /sprinkler/zone/1
@app.route("/sprinkler/zone/<zone>")
def get_zone(zone):
    return zone_control.get_zone(data, zone)

# POST /sprinkler/reset


#