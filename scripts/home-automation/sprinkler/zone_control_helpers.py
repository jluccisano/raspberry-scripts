import json
import sys
import time
import os
import RPi.GPIO as GPIO
from tqdm import tqdm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 23/16	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E


def get_zones_definition():
    json_data = {}
    data_tpl = os.path.join(os.path.abspath(os.path.dirname(__file__))) + '/data.json'
    with open(data_tpl) as data_file:
        json_data = json.load(data_file)
    return json_data["zones"]

def get_zone(zoneId):
    zoneData = {}
    for zone in get_zones_definition():
        if zone["id"] == int(zoneId):
            GPIO.setup(zone["boardOut"], GPIO.OUT)
            zone["value"] = not GPIO.input(int(zone["boardOut"]))
            zoneData = zone
            break
    return zoneData


def set_zone(zoneId, state):
    zoneData = {}
    for zone in get_zones_definition():
        if zone["id"] == int(zoneId):
            GPIO.setup(zone["boardOut"], GPIO.OUT)
            GPIO.output(zone["boardOut"], int(state))
            zone["value"] = not GPIO.input(int(zone["boardOut"]))
            zoneData = zone
            break
    return zoneData


def toggle_zone(zoneId):
    zoneData = {}
    for zone in get_zones_definition():
        if zone["id"] == int(zoneId):
            GPIO.setup(zone["boardOut"], GPIO.OUT)
            GPIO.output(zone["boardOut"], not GPIO.input(int(zone["boardOut"])))
            zone["value"] = not GPIO.input(int(zone["boardOut"]))
            zoneData = zone
            break
    return zoneData


def get_all_zones():
    chan_list = []
    zones = get_zones_definition()
    for zone in zones:
        chan_list.append(zone["boardOut"])
        GPIO.setup(chan_list, GPIO.OUT)

    for zone in zones:
        zone["value"] = not GPIO.input(int(zone["boardOut"]))

    return zones

def get_all_zones_state():
    chan_list = []
    zones = get_zones_definition()
    zones_state = []
    for zone in zones:
        chan_list.append(zone["boardOut"])
        GPIO.setup(chan_list, GPIO.OUT)

    for zone in zones:
        zones_state.append(not GPIO.input(int(zone["boardOut"])))

    return zones_state



def set_all_zones(state):
    chan_list = []
    zones = get_zones_definition()
    for zone in zones:
        chan_list.append(zone["boardOut"])
        GPIO.setup(chan_list, GPIO.OUT)
        GPIO.output(chan_list, int(state))
    return get_all_zones()


def run_step(zone, duration, description):
    print description
    print zone
    set_zone(zone, 0)
    interval = float(duration) / 100
    for i in tqdm(range(100)):
        time.sleep(interval)
        set_zone(zone, 1)


def run_scenario(json_scenario):
    print 'start run scenario'
    try:
        for step in json_scenario:
            print step
            run_step(step['zone'], step['duration'], step['description'])
    except KeyboardInterrupt:
        set_all_zones(1)
        sys.exit(0)
    print 'finish scenario'