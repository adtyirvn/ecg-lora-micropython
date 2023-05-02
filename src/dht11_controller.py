import dht
from machine import Pin
from time import sleep

class DHT11Sensor:
    def __init__(self, pin):
        self.sensor = dht.DHT11(Pin(pin))
    
    def read(self):
        self.sensor.measure()
        temperature = self.sensor.temperature()
        humidity = self.sensor.humidity()
        return temperature, humidity