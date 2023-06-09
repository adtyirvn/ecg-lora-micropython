from machine import SoftI2C, Pin
from src import ads1x15
from time import sleep
from src import display_ssd1306_i2c

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

adc = ads1x15.ADS1115(i2c, 72, 1)
oled = display_ssd1306_i2c.Display(i2c)

def show_on_oled(items, delay=0):
    oled.fill(0)
    for i, text in enumerate(items):
        oled.text(text, 0, 10 * i)
    oled.show()
    sleep(delay)

while True:
    raw = adc.read()
    print(raw)
    v = adc.raw_to_v(raw)
    print(v)
    show_on_oled([str(raw),str(v)],0)
    sleep(2)