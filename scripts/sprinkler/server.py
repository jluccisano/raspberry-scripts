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
@app.route("/sprinkler/zone/<zoneId>", methods = ['POST'])
def set_zone_by_id(zoneId):
    state = request.args.get('state', default=1, type=int)
    if state is None:
        return jsonify({'message': 'State param is mandatory'}, status=404)
    return jsonify(status=200, indent=4, sort_keys=True, result = set_zone(zoneId, state))

# POST /sprinkler/zone/1/toggle
@app.route("/sprinkler/zone/<zoneId>/toggle", methods = ['POST'])
def toggle_by_zone_id(zoneId):
    return jsonify(status=200, indent=4, sort_keys=True, result = toggle_zone(zoneId))

# POST /sprinkler/zones?state1
@app.route("/sprinkler/zones", methods = ['POST'])
def set_zones():
    state = request.args.get('state', default=1, type=int)
    if state is None:
        return jsonify({'message': 'State param is mandatory'}, status=404)
    return jsonify(status=200, indent=4, sort_keys=True, result = set_all_zones(state))

# GET /sprinkler/zone/1
@app.route("/sprinkler/zone/<zone>",  methods = ['GET'])
def get_zone_by_id(zone):
    return jsonify(status=200, indent=4, sort_keys=True, result = get_zone(zone))

# GET /sprinkler/zones
@app.route("/sprinkler/zones",  methods = ['GET'])
def get_zones():
    return jsonify(status=200, indent=4, sort_keys=True, result = get_all_zones())

# POST /sprinkler/reset
@app.route("/sprinkler/reset", methods = ['POST'])
def reset():
    return jsonify(status=200, indent=4, sort_keys=True, result = set_all_zones(1))


