#!/usr/bin/python
import RPi.GPIO as GPIO
import argparse
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 24/18	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

class RelayControl(object):

	def set(self):
		parser = argparse.ArgumentParser(
		    description='Set relay state high=1 or low=0')

		parser.add_argument('--relay', help='Set relay 1/2/3/4/5 or *', required=False)
		parser.add_argument('--state',help='Set state high=1 or low=0', required=False)

		args = parser.parse_args(sys.argv[2:])

		if args.relay == "*":
			print 'Set all relay to state=%s' % args.state
			setAll(args.state)
		else:
			print 'Set relay=%s to state=%s' % args.relay, args.state
			GPIO.setup(self.relayIO[relay], GPIO.OUT)
			GPIO.output(self.relayIO[relay], int(state))       
			GPIO.cleanup()

	def toggle(self):
		parser = argparse.ArgumentParser(
		    description='Toggle relay value')

		parser.add_argument('--relay', help='Set relay 1/2/3/4/5', required=False)

		args = parser.parse_args(sys.argv[2:])
		print 'Toggle relay=%s' % args.relay

		GPIO.setup(self.relayIO[relay], GPIO.OUT)
		GPIO.output(self.relayIO[relay], not GPIO.input(self.relayIO[relay]))
		GPIO.cleanup()

	def get(self):
		parser = argparse.ArgumentParser(
		    description='Set relay state high=1 or low=0')

		parser.add_argument('--relay', help='Set relay 1/2/3/4/5 or *', required=False)

		args = parser.parse_args(sys.argv[2:])

		if args.relay == "*":
			print 'Get all relay state'
			state = getAll()
		else:
			print 'Get relay=%s' % args.relay
			GPIO.setup(self.relayIO[relay], GPIO.OUT)
			state = GPIO.input(int(self.relayIO[relay]))
			GPIO.cleanup()
		return state

	def setAll(self, state):
		chan_list = []
		for relay in self.relayIO:
			chan_list.append(self.relayIO[relay])
		GPIO.setup(chan_list, GPIO.OUT)
		GPIO.output(chan_list, int(state))
		GPIO.cleanup()

	def getAll():
		chan_list = []
		state_list = []
		for relay in self.relayIO:
			chan_list.append(self.relayIO[relay])
		GPIO.setup(chan_list, GPIO.OUT)
		for relay in self.relayIO:
			state_list.append(GPIO.input(int(self.relayIO[relay])))
		GPIO.cleanup()
		return state_list

	def __init__(self):
		
		self.relayIO = { "1": 15, "2": 12, "3": 18, "4": 11, "5": 13}
		
		parser = argparse.ArgumentParser(
		    description='Relay control',
		    usage='''relay <command> [<args>]
		The most commonly used relay commands are:
		   set     Set relay value high or low
		   get     Get relay value high or low
		   toggle  Toggle relay value
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
    RelayControl()
