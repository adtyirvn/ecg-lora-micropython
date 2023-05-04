import dht
from machine import Pin
from time import sleep

class DHT11Sensor:
    def __init__(self, pin):
        self.sensor = dht.DHT11(Pin(pin))
        self.led = Pin(2, Pin.OUT)
    
    def read(self):
        try:
            self.sensor.measure()
            temperature = self.sensor.temperature()
            humidity = self.sensor.humidity()
            self.blink_led()
            return temperature, humidity
        except Exception as e:
            raise Exception("Error reading sensor: {}".format(e))
    
    def blink_led(self):
        self.led.on()
        sleep(0.5)
        self.led.off()