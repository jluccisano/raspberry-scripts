#!/usr/bin/python
import random

def getData_func():
    humidity =  random.uniform(0, 100)
    temperature =  random.uniform(-40, 40)
    if humidity is not None and temperature is not None:
        print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        return  { '@type':'DHT22', 'temperature': temperature, 'humidity': humidity }
    else:
        print('Failed to get reading. Try again!')
        return

if __name__ == "__main__": getData_func()