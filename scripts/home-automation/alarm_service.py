import ConfigParser
import os

from synology.camera import *

config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.conf'))

account = config.get('SYNOLOGY', 'account')
password = config.get('SYNOLOGY', 'password')
base_url = config.get('SYNOLOGY', 'base_url')

synoApi = SurveillanceCameraApi(base_url, account, password)

def disable_camera(id):
    return synoApi.disable_camera(id)

def enable_camera(id):
    return synoApi.enable_camera(id)


def get_camera_by_name(name):
    synoApi.get_camera_by_name(name)