import ConfigParser
import os
import sys
import time
import logging
from tqdm import tqdm

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

rain_data = weather_station.get_rain_data(station_id, pluvio_id)



# https://rainbird.com/sites/default/files/media/documents/2018-02/ts_3500.pdf
# pressure 3,5
# Nozzle 2
# precip 13-15mm/h
ROTOR_PRECIPITATION_RATE_BY_HOUR = 15
# Target 4mm/h
TARGET = 3

DROP_BY_DROP_RATE_BY_HOUR = 4
DROP_BY_DROP_TARGET = 3

def calculate_seconds_to_sprinkle(last_24_precip):
    return ((TARGET - last_24_precip) / float(ROTOR_PRECIPITATION_RATE_BY_HOUR)) * 3600

def calculate_seconds_to_sprinkle_drop_by_drop(last_24_precip):
    return ((DROP_BY_DROP_TARGET - last_24_precip) / float(DROP_BY_DROP_RATE_BY_HOUR)) * 3600

class SprinklerStepMachine:

    def is_running(self):
        return self._is_running

    def is_aborted(self):
        return self._is_aborted

    def set_aborted(self, val):
        self._is_aborted = val

    def stop(self):
        self._is_aborted = True

    def start(self):
        logging.info('start run scenario')

        rain_data = weather_station.get_rain_data(station_id, pluvio_id)
        last_24_precip = rain_data["sum_rain_24"]

        logging.info('get last 24 precipication: %d', last_24_precip)

        irrigate_duration = calculate_seconds_to_sprinkle(last_24_precip)
        drop_by_drop_duration = calculate_seconds_to_sprinkle_drop_by_drop(last_24_precip)

        logging.info('irrigate duration: %d', irrigate_duration)
        logging.info('drop_by_drop duration: %d', drop_by_drop_duration)

        self._is_running = True
        self._status = {}

        try:
            for zone in self._sprinklerControl.get_zones_definition():
                logging.info('Run: %s', zone['name'])
                self._status['zone'] = zone['name']
                logging.info(self._status)
                if zone["type"] == "irrigate":
                    self._run_step(zone['id'], irrigate_duration)
                elif zone["type"] == "drop_by_drop":
                    self._run_step(zone['id'], drop_by_drop_duration)
        except Exception:
            logging.info('Scenario aborted')
            self._sprinklerControl.set_all_zones(1)
            self._status = {}
        logging.info('finish scenario')
        self._is_running = False
        self._status = {}

    def _run_step(self, zone, duration):
        logging.info('starting step %s', zone)
        self._sprinklerControl.set_zone(zone, 0)
        interval = float(duration) / 100
        for i in tqdm(range(100)):
            if self._is_aborted:
                logging.info('is aborted')
                raise Exception('Aborted by user')
            time.sleep(interval)
            self._update_status((i * interval), duration)
        logging.info('finished step %s', zone)
        self._sprinklerControl.set_zone(zone, 1)

    def _update_status(self, current, duration):
        self._status['percent_completed'] = (current / float(duration) * 100)
        logging.info(self._status)

    def get_status(self):
        if self._is_running:
            logging.info(self._status)
            return self._status
        else:
            raise Exception('No scenario is running')

    def __init__(self):
        """Initialize a Weather station API."""
        print 'Starting Weather Station API'
        self._sprinklerControl = SprinklerControl()
        self._is_running = False
        self._is_aborted = False
        self._status = {}

sprinklerStepMachine = SprinklerStepMachine()

def run_scenario():
    sprinklerStepMachine.start()

def get_status():
    return sprinklerStepMachine.get_status()

def stop_scenario():
    sprinklerStepMachine.stop()

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