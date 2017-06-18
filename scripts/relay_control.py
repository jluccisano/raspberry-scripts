#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 24/18	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

relayIO = { "1": 15, "2": 2, "3": 18, "4": 11, "5": 13}

def setState(relay, state):
	GPIO.output(relayIO[relay], state)

	if getState(relay) != state:
		print("relay: " + relay + "is not set to " + state)

	print("relay: " + relay + "is set to " + getState(relay))

def getState(relay):
	return GPIO.input(relayIO[relay])

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--relay', help='Set relay 1/2/3/4/5', required=True)
    parser.add_argument('--state',help='Set state high=1 or low=0', required=True)

    args = parser.parse_args()

    setState(args.relay, args.state)

if __name__ == '__main__':
    main()
