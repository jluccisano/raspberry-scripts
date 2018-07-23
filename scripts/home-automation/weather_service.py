import ConfigParser
import os

from netatmo.weather_station import WeatherStationApi

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.conf'))

username = config.get('NETATMO', 'username')
password = config.get('NETATMO', 'password')
client_id = config.get('NETATMO', 'client_id')
client_secret = config.get('NETATMO', 'client_secret')
station_id = config.get('NETATMO', 'station_id')
pluvio_id = config.get('NETATMO', 'pluvio_id')

weather_station = WeatherStationApi(username, password, client_id, client_secret)

def get_rain():
    return weather_station.get_rain_data(station_id, pluvio_id)