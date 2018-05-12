from zone_control_helpers import *
from flask import Flask
from flask import request, make_response
from json import dumps


app = Flask(__name__)

def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

# POST /sprinkler/zone/1?state=1
@app.route("/sprinkler/zone/<zone>", methods = ['POST'])
def set_zone_by_id(zone):
    state = request.args.get('state')
    return "Hello World!" + state


# GET /sprinkler/zone/1
@app.route("/sprinkler/zone/<zone>",  methods = ['GET'])
def get_zone_by_id(zone):
    return jsonify(get_zone(zone))

# GET /sprinkler/zones
@app.route("/sprinkler/zones",  methods = ['GET'])
def get_zones():
    return jsonify(get_all_zones())

# POST /sprinkler/reset
@app.route("/sprinkler/reset", methods = ['POST'])
def reset():
    return jsonify(set_all_zones(1))


