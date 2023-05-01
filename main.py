import config
import uos

uos.chdir('src')

from wifi import WiFiConnection
ssid = config.wifi["SSID"]
password = config.wifi["PASSWORD"]

pin = 2

wife = WiFiConnection(ssid,password, pin)
wife.connect()
wife.disconnect()

