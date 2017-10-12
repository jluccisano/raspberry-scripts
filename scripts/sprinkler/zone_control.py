#!/usr/bin/env python
import RPi.GPIO as GPIO
import argparse
import sys
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 23/16	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

class ZoneControl(object):

	def set(self):
		parser = argparse.ArgumentParser(
		    description='Set zone state high=1 or low=0')

		parser.add_argument('--zone', help='Set zone 1/2/3/4/5 or *', required=False)
		parser.add_argument('--state',help='Set state high=1 or low=0', required=False)

		args = parser.parse_args(sys.argv[2:])

		if args.zone:
                    for zone in self.data["zones"]:
                        if zone["id"]==int(args.zone):
                            GPIO.setup(zone["boardOut"], GPIO.OUT)
			    GPIO.output(zone["boardOut"], int(args.state))
                            zone["value"] = GPIO.input(int(zone["boardOut"]))
                            print zone
		else:
		    self.setAll(args.state)
			
	def toggle(self):
		parser = argparse.ArgumentParser(
		    description='Toggle zone value')

		parser.add_argument('--zone', help='Set zone 1/2/3/4/5', required=False)

		args = parser.parse_args(sys.argv[2:])
                 
                if args.zone:
                    for zone in self.data["zones"]:
                        if zone["id"]==int(args.zone):
                            GPIO.setup(zone["boardOut"], GPIO.OUT)
                            GPIO.output(zone["boardOut"], not GPIO.input(int(zone["boardOut"])))
                            zone["value"] = GPIO.input(int(zone["boardOut"]))
                            print zone

	def get(self):
		parser = argparse.ArgumentParser(
		    description='Set zone state high=1 or low=0')

		parser.add_argument('--zone', help='Set zone 1/2/3/4/5 or *', required=False)

		args = parser.parse_args(sys.argv[2:])

		if args.zone:
                        for zone in self.data["zones"]:
                            if zone["id"]==int(args.zone):
                                GPIO.setup(zone["boardOut"], GPIO.OUT)
			        zone["value"]=GPIO.input(int(zone["boardOut"]))
                                print zone
		else:
			print self.getAll()
			

	def getAll(self):
		chan_list = []
		for zone in self.data["zones"]:
			chan_list.append(zone["boardOut"])
		GPIO.setup(chan_list, GPIO.OUT)

		for zone in self.data["zones"]:
			zone["value"] =  GPIO.input(int(zone["boardOut"]))

		return self.data["zones"]

	def setAll(self, state):
		chan_list = []
	
                for zone in self.data["zones"]:
                    chan_list.append(zone["boardOut"])
		GPIO.setup(chan_list, GPIO.OUT)
		GPIO.output(chan_list, int(state))
                print self.getAll()

	def __init__(self):

		with open('data.json') as data_file:
			self.data = json.load(data_file)

		parser = argparse.ArgumentParser(
		    description='Zone control',
		    usage='''zone <command> [<args>]
		The most commonly used zone commands are:
		   set     Set zone value high or low
		   get     Get zone value high or low
		   toggle  Toggle zone value
		''')
		parser.add_argument('command', help='Subcommand to run')
		# parse_args defaults to [1:] for args, but you need to
		# exclude the rest of the args too, or validation will fail
		args = parser.parse_args(sys.argv[1:2])
		if not hasattr(self, args.command):
			print 'Unrecognized command'
			parser.print_help()
			exit(1)
		# use dispatch pattern to invoke method with same name
		getattr(self, args.command)()
	
if __name__ == '__main__':
	ZoneControl()
