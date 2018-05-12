import RPi.GPIO as GPIO
import sys
import time
import json
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
    with open('data.json') as data_file:
        json_data = json.load(data_file)
    return json_data["zones"]

def get_zone(zoneId):
    zoneData = {}
    for zone in get_zones_definition():
        if zone["id"] == int(zoneId):
            GPIO.setup(zone["boardOut"], GPIO.OUT)
            zone["value"] = GPIO.input(int(zone["boardOut"]))
            zoneData = zone
            break
    return zoneData


def set_zone(zoneId, state):
    for zone in get_zones_definition():
        if zone["id"] == int(zoneId):
            GPIO.setup(zone["boardOut"], GPIO.OUT)
            GPIO.output(zone["boardOut"], int(state))
            zone["value"] = GPIO.input(int(zone["boardOut"]))
            zoneData = zone
            break
    return zoneData


def toggle_zone(zoneId):
    for zone in get_zones_definition():
        if zone["id"] == int(zoneId):
            GPIO.setup(zone["boardOut"], GPIO.OUT)
            GPIO.output(zone["boardOut"], not GPIO.input(int(zone["boardOut"])))
            zone["value"] = GPIO.input(int(zone["boardOut"]))
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
        zone["value"] = GPIO.input(int(zone["boardOut"]))

    return zones


def set_all_zones(state):
    chan_list = []
    zones = get_zones_definition()
    for zone in zones:
        chan_list.append(zone["boardOut"])
        GPIO.setup(chan_list, GPIO.OUT)
        GPIO.output(chan_list, int(state))
        print get_all_zones(zones)


def run_step(zone, duration, description):
    print description
    print zone
    zones = get_zones_definition()
    set_zone(zones, zone, 0)
    interval = float(duration) / 100
    for i in tqdm(range(100)):
        time.sleep(interval)
        set_zone(zones, zone, 1)


def run_scenario(json):
    scenario = {}
    print 'start run scenario'

    with open(json) as scenario_file:
        scenario = json.load(scenario_file)

    try:
        for step in scenario:
            print step
            run_step(step['zone'], step['duration'], step['description'])
    except KeyboardInterrupt:
        set_all_zones(1)
        sys.exit(0)

    print 'finish scenario'