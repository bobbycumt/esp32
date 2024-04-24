# -*- coding: utf-8 -*-
from machine import Pin,I2C
import utime
from lib import urequests
import ujson
import ssd1306
from umqtt.simple import MQTTClient
import dht

th=dht.DHT11(Pin(2))

# i2c=I2C(sda=Pin(21),scl=Pin(22))
# display=ssd1306.SSD1306_I2C(128,32,i2c)
# display.font_load("GB2312-12.fon")

ssid='bbhh'
psw='lb19850922'

SERVER = "bj-2-mqtt.iot-api.com"
PORT = 1883
CLIENT_ID = 'd9zr399x'
USERNAME = '7kvj6n16d8j2lwxe'
PASSWORD = '85mf2Hkk0p'
TOPIC = "attributes"
TOPIC1 = "attributes/push"

p13 = Pin(13, Pin.OUT)

f=0
state=0

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, psw)
        while not wlan.isconnected():
             p13.value(1)    
             utime.sleep(0.1)             
             p13.value(0)   
             utime.sleep(0.1)          
    print('network config:', wlan.ifconfig())
    if wlan.isconnected()==True:
        p13.value(0)

def mqtt_connect():
    client = MQTTClient(CLIENT_ID, SERVER, PORT, USERNAME, PASSWORD,keepalive=600)
    client.connect()
    print('Connected to MQTT Broker "{server}"'.format(server = SERVER))
    return client

def on_message(topic, msg):
    global f
    global state
    print("Received '{payload}' from topic '{topic}'\n".format(
        payload = msg.decode(), topic = topic.decode()))
    d=ujson.loads(msg.decode())
    k=list(d.keys())
    if k[0]=="get":
        f=2
    elif k[0]=="state":   
        f=1
        state=d["state"]
def subscribe(client):
    client.set_callback(on_message)
    client.subscribe(TOPIC1)

def main():
    global f
    do_connect()
    client= mqtt_connect()
    subscribe(client)
    while 1:
        th.measure()
        t=th.temperature()
        h=th.humidity()
        if f==1:
            p13.value(state)
            utime.sleep(1)
            p13.value(0)
            msg_dict = {
                    'state': 0
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print(1)
            f=0
        elif f==2:
            msg_dict = {
                    'tmp': t, 'humidity': h
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print("Send '{msg}' to topic '{topic}'".format(msg = msg, topic = TOPIC))
            print(2)
            f=0
        client.wait_msg()



if __name__=='__main__':
    main()