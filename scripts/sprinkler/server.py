from zone_control_helpers import *
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


# POST /sprinkler/zone/1?state=1
@app.route("/sprinkler/zone/<zone>", methods = ['POST'])
def set_zone_by_id(zone):
    state = request.args.get('state')
    return "Hello World!" + state


# GET /sprinkler/zone/1
@app.route("/sprinkler/zone/<zone>",  methods = ['GET'])
def get_zone_by_id(zone):
    return jsonify(get_zone(zone))

# POST /sprinkler/reset


