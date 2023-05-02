import uasyncio as asyncio
import config
import uos
import utime

uos.chdir('src')

from wifi_controller import WiFiConnection
from rtc_controller import RTCController
from dht11_controller import DHT11Sensor

ssid = config.WIFI["SSID"]
password = config.WIFI["PASSWORD"]

led_pin = 2
dht_pin = 5

wifi = WiFiConnection(ssid,password,led_pin)
rtc = RTCController()
dht = DHT11Sensor(dht_pin)

def main():
    wifi.connect()
    rtc.set_from_internet()
    wifi.disconnect()
    previous_time = utime.ticks_ms()
    while True:
        current_time = utime.ticks_ms()
        elapsed_time = current_time - previous_time
        if elapsed_time >= 2000:
            current_datetime = rtc.get_datetime()
            formatted_time = "{:02d}:{:02d}:{:02d}".format(
                current_datetime[4], current_datetime[5], current_datetime[6]
            )
            temp, humi = dht.read()
            print("Temp: {} Humi: {}".format(temp, humi))
            print("Current time:", formatted_time)
            previous_time = current_time
    
main()
# loop = asyncio.get_event_loop()
# loop.create_task(main())
# loop.run_forever()

