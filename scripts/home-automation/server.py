import atexit
import json
import logging
from json import dumps

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, send_file
from flask import make_response
from flask_swagger_ui import get_swaggerui_blueprint

from pytz import utc

from alarm_service import *
from auth import *
from sprinkler_service import *

logging.basicConfig(level=logging.INFO)

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(1),
    'processpool': ProcessPoolExecutor(1)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/resources/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.start()

app = Flask(__name__, static_url_path='/resources')

def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


@app.route('/resources/swagger.json')
def swagger_json():
    # Read before use: http://flask.pocoo.org/docs/0.12/api/#flask.send_file
    return send_file('resources/swagger.json')

# POST /sprinkler/zones/1?state=1
@app.route("/sprinkler/zones/<zoneId>", methods=['POST'])
@requires_auth
def set_zone_by_id(zoneId):
    state = request.args.get('state', default=1, type=int)
    if state is None:
        return jsonify({'message': 'State param is mandatory'}, status=404)
    return jsonify(status=200, indent=4, sort_keys=True, result=set_zone(zoneId, state))


# POST /sprinkler/zones/1/toggle
@app.route("/sprinkler/zones/<zoneId>/toggle", methods=['POST'])
@requires_auth
def toggle_by_zone_id(zoneId):
    return jsonify(status=200, indent=4, sort_keys=True, result=toggle_zone(zoneId))


# POST /sprinkler/zones?state1
@app.route("/sprinkler/zones", methods=['POST'])
@requires_auth
def set_zones():
    state = request.args.get('state', default=1, type=int)
    if state is None:
        return jsonify({'message': 'State param is mandatory'}, status=404)
    return jsonify(status=200, indent=4, sort_keys=True, result=set_all_zones(state))


# GET /sprinkler/zone/1
@app.route("/sprinkler/zones/<zone>", methods=['GET'])
@requires_auth
def get_zone_by_id(zone):
    return jsonify(status=200, indent=4, sort_keys=True, result=get_zone(zone))


# GET /sprinkler/zones
@app.route("/sprinkler/zones", methods=['GET'])
@requires_auth
def get_zones():
    format = request.args.get('format')
    if format is not None and format == 'lite':
        return jsonify(status=200, indent=4, sort_keys=True, result=get_all_zones_state())
    else:
        return jsonify(status=200, indent=4, sort_keys=True, result=get_all_zones())


# POST /sprinkler/reset
@app.route("/sprinkler/reset", methods=['POST'])
@requires_auth
def reset():
    return jsonify(status=200, indent=4, sort_keys=True, result=set_all_zones(1))


# POST /api/sprinkler/v2/scenario
@app.route("/api/sprinkler/v2/scenario", methods=['POST'])
@requires_auth
def mode_auto():
    body = request.get_json(force=True)
    force = request.args.get('force', bool)
    job = ""
    cron_expression = body['cron_expression']
    print cron_expression
    if cron_expression is None:
        return jsonify(status=404, indent=4, sort_keys=True, result={'message': 'Cron expression param is mandatory'})
    # run direct
    if force == True:
        job = scheduler.add_job(run_scenario, 'date')
    else:
        current = scheduler.get_job("myScenario", "default")
        print current
        if current:
            scheduler.remove_job("myScenario", "default")
        job = scheduler.add_job(run_scenario, trigger=CronTrigger.from_crontab(cron_expression), id="myScenario")
    print job
    return jsonify(status=200, indent=4, sort_keys=True, result=str(job))

# POST /api/sprinkler/v2/scenario
@app.route("/api/sprinkler/v3/disable", methods=['POST'])
@requires_auth
def mode_manu():
    sprinklerStepMachine.stop()
    current = scheduler.get_job("myScenario", "default")
    print current
    if current:
        scheduler.remove_job("myScenario", "default")
    return jsonify(status=200, indent=4, sort_keys=True)


# GET /sprinkler/zone/1
@app.route("/api/sprinkler/scenarios", methods=['GET'])
@requires_auth
def get_scenarios():
    return jsonify(status=200, indent=4, sort_keys=True, result=str(scheduler.get_jobs()))

# GET /sprinkler/zone/1
@app.route("/api/sprinkler/v4/status", methods=['GET'])
@requires_auth
def status():
    return jsonify(status=200, indent=4, sort_keys=True, result=get_status())

#### Synology surveillance camera

# GET /cameras?name='Camera Salon'
@app.route("/cameras", methods=['GET'])
@requires_auth
def get_camera_by_name():
    name = request.args.get('name')
    if name is None:
        return jsonify(status=404, indent=4, sort_keys=True, result={'message': 'Name param is mandatory'})
    return jsonify(status=200, indent=4, sort_keys=True, result=get_camera_by_name(name))


# POST /cameras/13/enable
@app.route("/cameras/<id>/enable", methods=['POST'])
@requires_auth
def enable_camera_by_id(id):
    return jsonify(status=200, indent=4, sort_keys=True, result=enable_camera(id))


# POST /cameras/13/disable
@app.route("/cameras/<id>/disable", methods=['POST'])
@requires_auth
def disable_camera_by_id(id):
    return jsonify(status=200, indent=4, sort_keys=True, result=disable_camera(id))


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8515)
