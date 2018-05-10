from unittest.mock import MagicMock
from zone_control import ZoneControl
import RPi.GPIO as GPIO

data = {}

with open('data.json') as data_file:
  data = json.load(data_file)

zone_control = ZoneControl()

GPIO.setup = MagicMock(return_value=3)
GPIO.input = MagicMock(return_value=3)

zone_control.get_zone(data, 1)
