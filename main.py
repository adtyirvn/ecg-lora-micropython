import uasyncio as asyncio
import ntptime
import dht
import machine
import network
import json

ssid = config.wifi["SSID"]
password = config.wifi.["PASSWORD"]
dht_pin = machine.Pin(<DHT11 data pin>, machine.Pin.IN)
dht_sensor = dht.DHT11(dht_pin)
rtc = machine.RTC()
rtc_set = False  # Flag to track RTC status

async def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            await asyncio.sleep(1)
    print("Wi-Fi connected.")
    print("IP address:", wlan.ifconfig()[0])

async def set_rtc_from_internet():
    global rtc_set
    if not rtc_set:
        try:
            ntptime.settime()  # Fetch the current time from an NTP server
            print("RTC set from internet time:", rtc.datetime())
            rtc_set = True  # Update the RTC status
        except OSError as e:
            print("Failed to set RTC from internet time:", e)
    else:
        print("RTC already set. Skipping...")

async def turn_off_wifi():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print("Disconnecting from Wi-Fi...")
        wlan.disconnect()
    wlan.active(False)
    print("Wi-Fi turned off.")

async def get_temperature():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    print("Temperature:", temperature)
    timestamp = rtc.datetime()
    timestamp_str = "{}-{}-{} {}:{}:{}".format(timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4], timestamp[5])
    data = {"temperature": temperature, "timestamp": timestamp_str}
    json_payload = json.dumps(data)
    print("JSON payload:", json_payload)
    json_bytes = json_payload.encode()
    print("JSON bytes:", json_bytes)

async def main():
    await connect_to_wifi()
    await set_rtc_from_internet()
    await turn_off_wifi()
    await get_temperature()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
