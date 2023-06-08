from machine import SoftI2C, Pin
from src import ads1x15
from time import sleep

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

adc = ads1x15.ADS1115(i2c, 72, 1)

while True:
    raw = adc.read()
    print(raw)
    print(adc.raw_to_v(raw))
    sleep(2)