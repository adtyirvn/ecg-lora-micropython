import config
import uos

uos.chdir('src')

from wifi import WiFiConnection
ssid = config.wifi["SSID"]
password = config.wifi["PASSWORD"]

wife = WiFiConnection(ssid,password)
wife.connect()
wife.disconnect()

