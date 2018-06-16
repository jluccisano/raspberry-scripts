import ConfigParser
import os
import sys
import time

from netatmo.weather_station import WeatherStationApi
from sprinkler.zone_control_helpers import SprinklerControl

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.conf'))

username = config.get('NETATMO', 'username')
password = config.get('NETATMO', 'password')
client_id = config.get('NETATMO', 'client_id')
client_secret = config.get('NETATMO', 'client_secret')
station_id = config.get('NETATMO', 'station_id')
pluvio_id = config.get('NETATMO', 'pluvio_id')

sprinklerControl = SprinklerControl()
weather_station = WeatherStationApi(username, password, client_id, client_secret)

# https://rainbird.com/sites/default/files/media/documents/2018-02/ts_3500.pdf
# pressure 3,5
# Nozzle 2
# precip 13-15mm/h
ROTOR_PRECIPITATION_RATE_BY_HOUR = 15
# Target 4mm/h
TARGET = 4

DROP_BY_DROP_RATE_BY_HOUR = 4
DROP_BY_DROP_TARGET = 4


def calculate_seconds_to_sprinkle(last_24_precip):
    return ((TARGET - last_24_precip) / ROTOR_PRECIPITATION_RATE_BY_HOUR) * 3600

def calculate_seconds_to_sprinkle_drop_by_drop(last_24_precip):
    return ((DROP_BY_DROP_TARGET - last_24_precip) / DROP_BY_DROP_RATE_BY_HOUR) * 3600

def run_scenario():
    print 'start run scenario'

    print "check rain data"
    rain_data = weather_station.get_rain_data(station_id, pluvio_id)
    last_24_precip = rain_data["sum_rain_24"]

    irrigate_duration = calculate_seconds_to_sprinkle(last_24_precip)
    drop_by_drop_duration = calculate_seconds_to_sprinkle_drop_by_drop(last_24_precip)

    try:
        for zone in sprinklerControl.get_zones_definition():
            if zone["type"] == "irrigate":
                _run_step(zone['id'], irrigate_duration)
            elif zone["type"] == "drop_by_drop":
                _run_step(zone['id'], drop_by_drop_duration)
    except KeyboardInterrupt:
        sprinklerControl.set_all_zones(1)
        sys.exit(0)
    print 'finish scenario'


def _run_step(zone, duration):
    print zone["description"]
    sprinklerControl.set_zone(zone, 1)
    time.sleep(float(duration))
    sprinklerControl.set_zone(zone, 0)


def set_zone(zoneId, state):
    return sprinklerControl.set_zone(zoneId, state)

def toggle_zone(zoneId):
    return sprinklerControl.toggle_zone(zoneId)

def set_all_zones(state):
    return sprinklerControl.set_all_zones(state)

def get_zone(zone):
    return sprinklerControl.get_zone(zone)

def get_all_zones_state():
    return sprinklerControl.get_all_zones_state()

def get_all_zones():
    return sprinklerControl.get_all_zones()