import sys
import os 
import time

IS_MICROPYTHON = (sys.implementation.name == 'micropython')
IS_ESP8266 = (os.uname().sysname == 'esp8266')
IS_ESP32 = (os.uname().sysname == 'esp32')

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:] 
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:] 

if IS_MICROPYTHON:
    # Node Name
    import machine
    import ubinascii 
    uuid = ubinascii.hexlify(machine.unique_id()).decode()  
        
    if IS_ESP8266:
        NODE_NAME = 'ESP8266_'
    if IS_ESP32:
        NODE_NAME = 'ESP32_'        
        
    NODE_EUI = mac2eui(uuid)
    NODE_NAME = NODE_NAME + uuid
    
    # millisecond
    millisecond = time.ticks_ms
    
    # Controller
    SOFT_SPI = None
    from .controller_esp import Controller
    

    
    