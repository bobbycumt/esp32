from umqtt.simple import MQTTClient
from machine import Pin
import network
import utime
import random


up = Pin(15, Pin.OUT)
down = Pin(4, Pin.OUT)
lock = Pin(2, Pin.OUT)
stop = Pin(5, Pin.OUT)

ssid = 'bbhh'
password = 'lb19850922'

client_id='pc_esp32' 
server = 'bj-2-mqtt.iot-api.com' 
port = 1883 #连接的端口
user = 'gi9ruf6zithfmw64' #产品的数字ID
pwd = 'VW6nAnxPSC'

# Received messages from subscriptions will be delivered to this callback
c = MQTTClient(client_id, server,port,user,pwd,60) 

def sub_cb(topic, msg):
    print((topic, msg))
    

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def main():
    do_connect()
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe("attributes/push")
    pt=0
    ct=utime.ticks_ms()
    while True:
        c.check_msg()
        ct=utime.ticks_ms()
        if ct-pt>5000:
            pt=utime.ticks_ms()
            c.publish(b"attributes", '{"temp": '+str(int(random.random()*100))+'}')
    
if __name__ == '__main__':
    main()