from json import dumps

from flask import Flask
from flask import make_response

from auth import *
from sprinkler.zone_control_helpers import *
from synology.camera import *

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.conf'))

app = Flask(__name__)

account = config.get('SYNOLOGY', 'account')
password = config.get('SYNOLOGY', 'password')
base_url = config.get('SYNOLOGY', 'base_url')

synoApi = SurveillanceCameraApi(base_url, account, password)

def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

# POST /sprinkler/zones/1?state=1
@app.route("/sprinkler/zones/<zoneId>", methods = ['POST'])
@requires_auth
def set_zone_by_id(zoneId):
    state = request.args.get('state', default=1, type=int)
    if state is None:
        return jsonify({'message': 'State param is mandatory'}, status=404)
    return jsonify(status=200, indent=4, sort_keys=True, result = set_zone(zoneId, state))

# POST /sprinkler/zones/1/toggle
@app.route("/sprinkler/zones/<zoneId>/toggle", methods = ['POST'])
@requires_auth
def toggle_by_zone_id(zoneId):
    return jsonify(status=200, indent=4, sort_keys=True, result = toggle_zone(zoneId))

# POST /sprinkler/zones?state1
@app.route("/sprinkler/zones", methods = ['POST'])
@requires_auth
def set_zones():
    state = request.args.get('state', default=1, type=int)
    if state is None:
        return jsonify({'message': 'State param is mandatory'}, status=404)
    return jsonify(status=200, indent=4, sort_keys=True, result = set_all_zones(state))

# GET /sprinkler/zone/1
@app.route("/sprinkler/zones/<zone>",  methods = ['GET'])
@requires_auth
def get_zone_by_id(zone):
    return jsonify(status=200, indent=4, sort_keys=True, result = get_zone(zone))

# GET /sprinkler/zones
@app.route("/sprinkler/zones",  methods = ['GET'])
@requires_auth
def get_zones():
    format = request.args.get('format')
    if format is not None and format == 'lite':
        return jsonify(status=200, indent=4, sort_keys=True, result = get_all_zones_state())
    else:
        return jsonify(status=200, indent=4, sort_keys=True, result = get_all_zones())

# POST /sprinkler/reset
@app.route("/sprinkler/reset", methods = ['POST'])
@requires_auth
def reset():
    return jsonify(status=200, indent=4, sort_keys=True, result = set_all_zones(1))

# POST /sprinkler/scenario
@app.route("/sprinkler/scenario", methods = ['POST'])
@requires_auth
def scenario():
    json_scenario = request.get_json(silent=True)
    if json_scenario is None:
        json_scenario = json.load(request.form.get('data'))
    return jsonify(status=200, indent=4, sort_keys=True, result = run_scenario(json_scenario))


#### Synology surveillance camera

# GET /cameras?name='Camera Salon'
@app.route("/cameras", methods = ['GET'])
@requires_auth
def get_camera_by_name():
    name = request.args.get('name')
    if name is None:
        return jsonify( status=404, indent=4, sort_keys=True, result = {'message': 'Name param is mandatory'})
    return jsonify(status=200, indent=4, sort_keys=True, result = synoApi.get_camera_by_name(name))

# POST /cameras/13/enable
@app.route("/cameras/<id>/enable", methods = ['POST'])
@requires_auth
def enable_camera_by_id(id):
    return jsonify(status=200, indent=4, sort_keys=True, result = synoApi.enable_camera(id))

# POST /cameras/13/disable
@app.route("/cameras/<id>/disable", methods = ['POST'])
@requires_auth
def disable_camera_by_id(id):
    return jsonify(status=200, indent=4, sort_keys=True, result = synoApi.disable_camera(id))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8515)