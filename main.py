import config
import utime
import ujson as json

# IMPORT PACKAGE
from src import wifi_controller
from src import rtc_controller
from src import dht11_controller
from src import sx127x
from src import config_lora
from src import LoRaSender

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
    dht = dht11_controller.DHT11Sensor(dht_pin)

    # SETUP
    try:
        print(node_name)
        wifi.connect()
        rtc.set_from_internet()
        rtc.get_formatted_datetime()
        wifi.disconnect()
        previous_time = utime.ticks_ms()
        while True:
            current_time = utime.ticks_ms()
            elapsed_time = current_time - previous_time
            if elapsed_time >= delay_ms:
                send_callback(lora, rtc, dht, node_name)
                previous_time = current_time
    except Exception as e:
        print(e)

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

def send_callback(lora, rtc_service, dht_service, name):
    payload = get_json_data(dht_service, rtc_service, name)
    print("Sending packet: {}".format(payload))
    lora.println(payload.encode('utf-8'))
        
main()
