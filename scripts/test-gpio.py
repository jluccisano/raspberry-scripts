#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)

print(GPIO.input(12))

GPIO.output(12, GPIO.LOW)

print(GPIO.input(12))

GPIO.output(12, GPIO.HIGH)

print(GPIO.input(12))