import network
from machine import Pin
import time

class WiFiConnection:
    def __init__(self, ssid, password, led_pin):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.led = Pin(led_pin, Pin.OUT)
    
    def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print("Connecting to Wi-Fi...")
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected():
                self.led.on()
                time.sleep(0.2)
                self.led.off()
                time.sleep(0.2)
       
        print("Wi-Fi connected.")
        print("IP address:", self.wlan.ifconfig()[0])
            
    def disconnect(self):
        if self.wlan.isconnected():
            print("Disconnecting from Wi-Fi...")
            self.wlan.disconnect()
        self.wlan.active(False)
        print("Wi-Fi turned off.")