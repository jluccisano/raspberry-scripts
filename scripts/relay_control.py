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
	GPIO.setup(relayIO[relay], GPIO.OUT)
	
	print("Trying to set relay: " + str(relayIO[relay]) + " to state: " + state)
	GPIO.output(relayIO[relay], int(state))
       
	if getState(relay) != state:
		print("relay: " + relay + " is not set to " + state)

	print("relay: " + relay + " is set to " + str(getState(relay)))

def getState(relay):
	return GPIO.input(int(relayIO[relay]))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', help='Set relay 1/2/3/4/5', required=True)
    parser.add_argument('-s',help='Set state high=1 or low=0', required=True)

    args = parser.parse_args()

    setState(args.relay, args.state)
    
    GPIO.cleanup()

if __name__ == '__main__':
    main()
