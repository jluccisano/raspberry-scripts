import json
import os

import RPi.GPIO as GPIO


# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 23/16	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

class SprinklerControl:
    """ TODO """

    def __init__(self):
        """Initialize a Sprinkler control API."""
        print 'Starting RPI GPIO'
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for zone in self.get_zones_definition():
            GPIO.setup(zone["boardOut"], GPIO.OUT, initial=1)
            zone["value"] = not GPIO.input(int(zone["boardOut"]))

    def get_zones_definition(self):
        json_data = {}
        data_tpl = os.path.join(os.path.abspath(os.path.dirname(__file__))) + '/data.json'
        with open(data_tpl) as data_file:
            json_data = json.load(data_file)
        return json_data["zones"]

    def get_zone(self, zoneId):
        zoneData = {}
        for zone in self.get_zones_definition():
            if zone["id"] == int(zoneId):
                zone["value"] = not GPIO.input(int(zone["boardOut"]))
                zoneData = zone
                break
        return zoneData

    def set_zone(self, zoneId, state):
        zoneData = {}
        for zone in self.get_zones_definition():
            if zone["id"] == int(zoneId):
                GPIO.output(zone["boardOut"], int(state))
                zone["value"] = not GPIO.input(int(zone["boardOut"]))
                zoneData = zone
                break
        return zoneData

    def toggle_zone(self, zoneId):
        zoneData = {}
        for zone in self.get_zones_definition():
            if zone["id"] == int(zoneId):
                GPIO.output(zone["boardOut"], not GPIO.input(int(zone["boardOut"])))
                zone["value"] = not GPIO.input(int(zone["boardOut"]))
                zoneData = zone
                break
        return zoneData

    def get_all_zones(self):
        zones = self.get_zones_definition()
        for zone in zones:
            zone["value"] = not GPIO.input(int(zone["boardOut"]))

        return zones

    def get_all_zones_state(self):
        zones = self.get_zones_definition()
        zones_state = []
        for zone in zones:
            zones_state.append(not GPIO.input(int(zone["boardOut"])))
        return zones_state

    def set_all_zones(self, state):
        chan_list = []
        zones = self.get_zones_definition()
        for zone in zones:
            chan_list.append(zone["boardOut"])
            GPIO.output(chan_list, int(state))
        return self.get_all_zones()
