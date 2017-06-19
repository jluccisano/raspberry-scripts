#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# GPIO/BOARD | Relay IN | Rotors | Zone
# 22/15	     | R2 IN2   | 1      | B
# 18/12	     | R1 IN2   | 2      | A
# 24/18	     | R1 IN3   | 3      | D
# 17/11	     | R1 IN4   | 4      | C
# 27/13	     | R2 IN1   | 5      | E

relayIO = { "1": 15, "2": 12, "3": 18, "4": 11, "5": 13}

def getState(relay):
    return GPIO.input(int(relayIO[relay]))

def main():
    print "relay 1: " + getState("1")
    print "relay 2: " + getState("2")
    print "relay 3: " + getState("3")
    print "relay 4: " + getState("4")
    print "relay 5: " + getState("5")


if __name__ == '__main__':
    main()
