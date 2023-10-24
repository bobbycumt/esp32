import time
import network
import ujson as json
import machine as mc
import urequests as requests
import ssd1306
from umqtt.simple import MQTTClient
import random
from machine import Pin

led=Pin(2,Pin.OUT)
ProductKey = "a12LxuejL2h"
ClientId = "a12LxuejL2h.dev1|securemode=2,signmethod=hmacsha256,timestamp=1654139505689|"
DeviceName = "dev1"
DeviceSecret = "0b097b47ea592cd53378ab85809bb387"

strBroker = ProductKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
Brokerport = 1883

user_name = "dev1&a12LxuejL2h"
user_password = "38f2f38093d08eaee93bc98bdffe90b6ba2905a06ddac374d8ac2e6db95d17da"
subscribe_TOPIC = "/sys/"+ProductKey+"/"+DeviceName+"/thing/service/property/set"

print("clientid:",ClientId,"\n","Broker:",strBroker,"\n","User Name:",user_name,"\n","Password:",user_password,"\n")

def connect():
    global led
    global client
    client = MQTTClient(client_id = ClientId,server= strBroker,port=Brokerport,user=user_name, password=user_password,keepalive=60) 
    #please make sure keepalive value is not 0
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(subscribe_TOPIC)
    while True:
        temperature =random.random()*100
        oled_show(str(temperature), 0, 10)
        send_mseg = '{"params": {"temperature": %s},"method": "thing.event.property.post"}' % (temperature)
        client.publish(topic="/sys/"+ProductKey+"/"+DeviceName+"/thing/event/property/post", msg=send_mseg,qos=1, retain=False)
        send_mseg = '{"params": {"GeoLocation": {"Longitude":%s,"Latitude":%s,"Altitude":%s}},"method": "thing.event.property.post"}' % (118.17,39.5,0)
        client.publish(topic="/sys/"+ProductKey+"/"+DeviceName+"/thing/event/property/post", msg=send_mseg,qos=1, retain=False)
        
        if led.value() == 1:
            send_mseg = '{"params": {"lightStatus": 1},"method": "thing.event.property.post"}'
            client.publish(topic="/sys/"+ProductKey+"/"+DeviceName+"/thing/event/property/post", msg=send_mseg,qos=1, retain=False)
        else:
            send_mseg = '{"params": {"lightStatus": 0},"method": "thing.event.property.post"}'
            client.publish(topic="/sys/"+ProductKey+"/"+DeviceName+"/thing/event/property/post", msg=send_mseg,qos=1, retain=False)
        time.sleep(3)


def OLEDInit():
    res=mc.Pin(19, mode=mc.Pin.OUT, pull=None, value=1) 
 
    i2c = mc.I2C(scl=mc.Pin(22), sda=mc.Pin(21), freq=400000)
    addr=i2c.scan()
    for x in addr:
         if x==60 :
            print('OLED exist!')
            break
         else:
            print('OLED not exist!')
    global oled
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)


def oled_show(data, row, col):
    oled.fill(0)
    oled.text(data, row, col)
    oled.show()

def wifi_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    oled_show(wlan.ifconfig()[0], 0, 0)

def sub_cb(topic, msg):
        global led
        global client
        msg = json.loads(msg)
        print(msg)
        if msg['params']['lightStatus'] ==1:
            print('receive ON')
            led.value(1)
            print('led ON')
            
        if msg['params']['lightStatus'] ==0:
            print('receive OFF')
            led.value(0)
            print('led OFF')
            

def main():
    global client
    global led
    ssid     = "bbhh"
    password = "lb19850922"

    OLEDInit()

    wifi_connect(ssid, password)  
    connect() 


if __name__ == "__main__":
    main()
