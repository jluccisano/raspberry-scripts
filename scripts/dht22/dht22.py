#!/usr/bin/python
import Adafruit_DHT

def getData_func():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    if humidity is not None and temperature is not None:
        print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        return  { '@type':'DHT22', 'temperature': temperature, 'humidity': humidity }
    else:
        print('Failed to get reading. Try again!')
        return

if __name__ == "__main__": getData_func()
