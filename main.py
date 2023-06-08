import config
# import utime
import ujson as json
# import struct

# IMPORT PACKAGE
from src import ads1x15
from src import wifi_controller
from src import rtc_controller
from src import dht11_controller
from src import sx127x
from src import config_lora
from src import display_ssd1306_i2c
from src import ascon
# import binascii
from time import sleep
from machine import Pin, SoftI2C
# from src import LoRaSender

# CONFIG
ssid = config.WIFI_SSID
password = config.WIFI_PASSWORD
led_pin = config.LED_PIN
dht_pin = config.DHT_PIN

led = Pin(led_pin, Pin.OUT)

delay_ms = 2000

# LoRa
controller = config_lora.Controller()
lora = controller.add_transceiver(sx127x.SX127x(name='LoRa'),
                                  pin_id_ss=config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone=config_lora.Controller.PIN_ID_FOR_LORA_DIO0)

# WiFi
wifi = wifi_controller.WiFiConnection(ssid, password, led_pin)

# RTC
rtc = rtc_controller.RTCController()

# SENSOR
dht = dht11_controller.DHT11Sensor(dht_pin, led_pin)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
adc = ads1x15.ADS1115(i2c, 72, 1)
oled = display_ssd1306_i2c.Display(i2c)

# ENKRIPSI
asc = ascon.Ascon()
master_node = "raspi"
node_one = "esp32"

key = config.ENCRYPT_KEY
nonce_g = config.ENCRYPT_NONCE

node_name = config_lora.NODE_NAME


def main():
    try:
        show_on_oled(["Starting..."])
        blink_led(3, 0.5, 0.5)

        show_on_oled(["Connecting to", f"{ssid} wifi..."])
        status, ip = wifi.connect()
        show_on_oled([status, ip], delay=1)

        rtc.set_from_internet()
        date = rtc.get_formatted_date()
        time = rtc.get_formatted_time()
        show_on_oled([date, time], delay=1)

        status = wifi.disconnect()
        show_on_oled([status], delay=1)

        show_on_oled(["Ready..."], delay=1)
        print("Ready...")

        while True:
            try:
                on_receive(lora, asc, key, nonce_g)
            except Exception as e:
                print(f"Error: {e}")
                show_on_oled(["Error:", "Sensor error..."])
    except KeyboardInterrupt:
        oled.clear()
        show_on_oled(["Goodbye..."], 5)
        oled.clear()
        led.off()


def show_on_oled(items, delay=0):
    oled.fill(0)
    for i, text in enumerate(items):
        oled.text(text, 0, 10 * i)
    oled.show()
    sleep(delay)


def blink_led(times=1, on_seconds=0.1, off_seconds=0.1):
    for i in range(times):
        led.on()
        sleep(on_seconds)
        led.off()
        sleep(off_seconds)


def on_receive(lora, enc, key, nonce):
    if lora.receivedPacket():
        global nonce_g
        payload = lora.read_payload()
        if not len(payload):
            return
        pay_json = payload.decode("utf-8")
        pay_dict = json.loads(pay_json)
        print(f"***Received packet***\n{pay_dict}")
        rst = pay_dict.get("rst")
        recipient = pay_dict["to"]
        sender = pay_dict["id"]
        if recipient != node_one and recipient != master_node:
            return
        if sender == master_node:
            nonce_gg = send_callback(lora, enc, key, config.ENCRYPT_NONCE if bool(rst) else nonce)
            nonce_g = nonce_gg


def send_callback(lora, enc, key, nonce):
    payload = get_json_data()
    ciphertext, new_nonce = encryption(
        enc, payload.encode("utf-8"), key, nonce, "CBC")
    print(
        f"***Sending packet***\n{payload.encode('utf-8')} len: {len(payload.encode('utf-8'))}")
    lora.println(ciphertext)
    message = json.loads(payload)
    print(message)
    show_info(message)
    return new_nonce


def encryption(ascon, message, key, nonce, mode="ECB"):
    print(f"key: {key} len: {len(key)}")
    print(f"nonce: {nonce} len: {len(nonce)}")
    ciphertext = ascon.ascon_encrypt(
        key, nonce, associateddata=b"", plaintext=message,  variant="Ascon-128")
    if mode == "CBC":
        new_nonce = ciphertext[:16]
        print(f"nw: {new_nonce} len: {len(new_nonce)}")
    return ciphertext, new_nonce


def get_json_data():
    dt = rtc.get_datetime()
    # temperature, humidity = dht.read()
    temperature = adc.read()
    humidity = adc.raw_to_v(temperature)
    data = {
        "id": node_one,
        "to": master_node,
        "t": temperature,
        "h": humidity,
        "tsp": dt
    }
    json_data = json.dumps(data)
    return json_data

def show_info(message):
    date = f"{get_formatted_date(message['tsp'])}"
    time = f"{get_formatted_time(message['tsp'])}"
    t = f"T: {message['t']}C"
    h = f"H: {message['h']}%"
    show_on_oled([date, time, t, h])

def get_formatted_date(date_tuple):
    return f"{date_tuple[0]:04d}-{date_tuple[1]:02d}-{date_tuple[2]:02d}"

def get_formatted_time(time_tuple):
    return f"{time_tuple[4]:02d}:{time_tuple[5]:02d}:{time_tuple[6]:02d}"
