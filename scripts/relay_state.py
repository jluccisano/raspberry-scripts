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

GPIO.setup(relayIO["1"], GPIO.OUT)
GPIO.setup(relayIO["2"], GPIO.OUT)
GPIO.setup(relayIO["3"], GPIO.OUT)
GPIO.setup(relayIO["4"], GPIO.OUT)
GPIO.setup(relayIO["5"], GPIO.OUT)

def getState(relay):
    return GPIO.input(int(relayIO[relay]))

def main():
    print "relay 1: " + str(getState("1"))
    print "relay 2: " + str(getState("2"))
    print "relay 3: " + str(getState("3"))
    print "relay 4: " + str(getState("4"))
    print "relay 5: " + str(getState("5"))


if __name__ == '__main__':
    main()
