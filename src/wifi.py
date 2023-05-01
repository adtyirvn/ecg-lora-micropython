import network

class WiFiConnection:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
    
    def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print("Connecting to Wi-Fi...")
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected():
                pass
        print("Wi-Fi connected.")
        print("IP address:", self.wlan.ifconfig()[0])
            
    def disconnect(self):
        if self.wlan.isconnected():
            print("Disconnecting from Wi-Fi...")
            self.wlan.disconnect()
        self.wlan.active(False)
        print("Wi-Fi turned off.")