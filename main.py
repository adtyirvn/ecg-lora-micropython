import config
import utime
import ujson as json

# IMPORT PACKAGE
from src import wifi_controller
from src import rtc_controller
from src import dht11_controller
from src import sx127x
from src import config_lora
from src import display_ssd1306_i2c
from machine import Pin, SoftI2C
# from src import LoRaSender

def main():
    # CONFIG
    ssid = config.WIFI_SSID
    password = config.WIFI_PASSWORD
    led_pin = config.LED_PIN
    dht_pin = config.DHT_PIN

    delay_ms = 2000

    # LoRa
    controller = config_lora.Controller()
    lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)
    
    node_name = config_lora.NODE_NAME

    # WiFi
    wifi = wifi_controller.WiFiConnection(ssid, password, led_pin)

    # RTC
    rtc = rtc_controller.RTCController()

    # SENSOR
    dht = dht11_controller.DHT11Sensor(dht_pin, led_pin)
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    oled = display_ssd1306_i2c.Display(i2c)
    # SETUP
    print(node_name)
    oled.fill(0)
    oled.show_text('starting...', 0, 0)
    oled.show()
    wifi.connect()
    rtc.set_from_internet()
    rtc.get_formatted_datetime()
    wifi.disconnect()
    previous_time = utime.ticks_ms()
    while True:
                try:
                    current_time = utime.ticks_ms()
                    elapsed_time = current_time - previous_time
                    if elapsed_time >= delay_ms:
                        send_callback(lora, rtc, dht, node_name, oled)
                        previous_time = current_time
                
                except Exception as e:
                    print(e)
                except KeyboardInterrupt:
                    oled.clear()
                    print("Exit")
                    break

def get_json_data(dht_service, rtc_service, id):
    current_datetime = rtc_service.get_datetime()
    temperature, humidity = dht_service.read()
    data = {
            "id": id,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": current_datetime
        }
    json_data = json.dumps(data)
    return json_data

def send_callback(lora, rtc_service, dht_service, name, oled):
    payload = get_json_data(dht_service, rtc_service, name)
    print("Sending packet: {}".format(payload))
    lora.println(payload.encode('utf-8'))
    message = json.loads(payload)
    date = f"{get_formatted_date(message['timestamp'])}"
    time = f"{get_formatted_time(message['timestamp'])}"
    t = f"T: {message['temperature']}C"
    h = f"H: {message['humidity']}%"
    oled.fill(0)
    # oled.show_text(text = date, clear_first = False)
    # oled.show_text(text = time, clear_first = False, x=0, y=10)  
    # oled.show_text(text = t, clear_first = False, x=0, y=20)  
    # oled.show_text(text = h, clear_first = False, x=0, y=30)
    oled.text(date, 0, 0) 
    oled.text(time, 0, 10) 
    oled.text(t, 0, 20) 
    oled.text(h, 0, 30) 
    oled.show()

def get_formatted_date(d):
    date_tuple = d
    formatted_date = "{:04d}-{:02d}-{:02d}".format(
        date_tuple[0], date_tuple[1], date_tuple[2])
    return formatted_date
def get_formatted_time(t):
    time_tuple = t
    formatted_time = "{:02d}:{:02d}:{:02d}".format(
        time_tuple[4], time_tuple[5], time_tuple[6])
    return formatted_time