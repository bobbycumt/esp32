# -*- coding: utf-8 -*-
from machine import Pin,I2C
import utime
from lib import urequests
import ujson
import ssd1306
from umqtt.simple import MQTTClient
import _thread

i2c=I2C(sda=Pin(21),scl=Pin(22))
display=ssd1306.SSD1306_I2C(128,32,i2c)
display.font_load("GB2312-12.fon")

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

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, psw)
        while not wlan.isconnected():
             p13.value(1)    
             time.sleep(0.1)             
             p13.value(0)   
             time.sleep(0.1)          
    print('network config:', wlan.ifconfig())
    if wlan.isconnected()==True:
        p13.value(0)

def mqtt_connect():
    client = MQTTClient(CLIENT_ID, SERVER, PORT, USERNAME, PASSWORD)
    client.connect()
    print('Connected to MQTT Broker "{server}"'.format(server = SERVER))
    return client

def on_message(topic, msg):
    print("Received '{payload}' from topic '{topic}'\n".format(
        payload = msg.decode(), topic = topic.decode()))

def subscribe(client):
    client.set_callback(on_message)
    client.subscribe(TOPIC1)
    
def loop_publish(client):
    msg_count = 0
    msg_count1 = 0
    t=5000
    tt=10000
    t1=utime.ticks_ms()
    tt1=utime.ticks_ms()
    while True:        
        msg_dict = {
            'tmp': msg_count
        }
        msg_dict1 = {
        'humidity': msg_count1
        }
        msg = ujson.dumps(msg_dict)
        msg1 = ujson.dumps(msg_dict1)
        client.check_msg()
        t2=utime.ticks_ms()
        tt2=utime.ticks_ms()
        display.fill(0)
        display.text(str(msg_count),0,0)
        display.show() 
        if utime.ticks_diff(tt2,tt1)>=tt:
            msg_count1+=1
            result = client.publish(TOPIC, msg1)
            print("Send '{msg}' to topic '{topic}'".format(msg = msg1, topic = TOPIC))
            tt1=utime.ticks_ms()
        if utime.ticks_diff(t2,t1)>=t:
            msg_count += 1
            result = client.publish(TOPIC, msg)
            print("Send '{msg}' to topic '{topic}'".format(msg = msg, topic = TOPIC))
            t1=utime.ticks_ms()
def waitmsg():
    client.wait_msg()
    
def main():
#     do_connect()
#     client = mqtt_connect()
#     subscribe(client)
#     loop_publish(client)
    msg_count = 0
    msg_count1 = 0
    t=5000
    tt=10000
    t1=utime.ticks_ms()
    tt1=utime.ticks_ms()
    while True:        
        msg_dict = {
            'tmp': msg_count
        }
        msg_dict1 = {
        'humidity': msg_count1
        }
        msg = ujson.dumps(msg_dict)
        msg1 = ujson.dumps(msg_dict1)
#         client.check_msg()
        t2=utime.ticks_ms()
        tt2=utime.ticks_ms()
        display.fill(0)
        display.text(str(msg_count),0,0)
        display.text(str(msg_count1),0,20)
        display.show() 
        if utime.ticks_diff(tt2,tt1)>=tt:
            msg_count1+=1
#             result = client.publish(TOPIC, msg1)
            print("Send '{msg}' to topic '{topic}'".format(msg = msg1, topic = TOPIC))
            tt1=utime.ticks_ms()
        if utime.ticks_diff(t2,t1)>=t:
            msg_count += 1
#             result = client.publish(TOPIC, msg)
            print("Send '{msg}' to topic '{topic}'".format(msg = msg, topic = TOPIC))
            t1=utime.ticks_ms()

if __name__=='__main__':
    main()