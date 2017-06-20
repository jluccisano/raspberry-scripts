#!/usr/bin/python
import RPi.GPIO as GPIO
import argparse

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 24/18	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

relayIO = { "1": 15, "2": 12, "3": 18, "4": 11, "5": 13}

def setState(relay, state):
	print("Trying to set relay: " + str(relayIO[relay]) + " to state: " + state)
	GPIO.output(relayIO[relay], int(state))
       
	if getState(relay) != state:
		print("relay: " + relay + " is not set to " + state)

	print("relay: " + relay + " is set to " + str(getState(relay)))

def toggle(relay):
	GPIO.output(relayIO[relay], not GPIO.input(relayIO[relay]))
	
def getState(relay):
	return GPIO.input(int(relayIO[relay]))

def setAll(state):
	chan_list = []
	for relay in relayIO:
    		chan_list.append(relayIO[relay])		
	GPIO.output(chan_list, int(state))

def getAll():
	chan_list = []
	for relay in relayIO:
    		chan_list.append(relayIO[relay])
	GPIO.setup(chan_list, GPIO.OUT)
	
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--relay', help='Set relay 1/2/3/4/5', required=True)
    parser.add_argument('--state',help='Set state high=1 or low=0', required=false)
    parser.add_argument('--toggle',help='Toggle state', required=false)
    parser.add_argument('--info',help='Get state high=1 or low=0', required=false)
    parser.add_argument('--all',help='Set all to state high=1 or low=0', required=false)

    args = parser.parse_args()
    GPIO.setup(relayIO[relay], GPIO.OUT)
    
    if args.toggle:
	toggle(args.relay)
    elif args.state:
	setState(args.relay, args.state)
    elif args.info:
	getState(args.relay)
    elif args.all and args.state:
	setAll(args.state)

    GPIO.cleanup()

if __name__ == '__main__':
    main()
