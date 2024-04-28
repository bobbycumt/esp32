# -*- coding: utf-8 -*-
from machine import Pin,I2C
import utime
# from lib import urequests
import ujson
# import ssd1306
from umqtt.simple import MQTTClient
import dht

th=dht.DHT11(Pin(18))
person=Pin(19, Pin.IN)
up = Pin(15, Pin.OUT)
down = Pin(4, Pin.OUT)
lock = Pin(2, Pin.OUT)
stop = Pin(5, Pin.OUT)
p13 = Pin(13, Pin.OUT)

# i2c=I2C(sda=Pin(21),scl=Pin(22))
# display=ssd1306.SSD1306_I2C(128,32,i2c)
# display.font_load("GB2312-12.fon")

ssid='CU_future'
psw='13582579999'
# ssid = 'bbhh'
# psw = 'lb19850922'

SERVER = "bj-2-mqtt.iot-api.com"
PORT = 1883
CLIENT_ID = 'scmcfuso'
USERNAME = 'gi9ruf6zithfmw64'
PASSWORD = 'VW6nAnxPSC'
TOPIC = "attributes"
TOPIC1 = "attributes/push"

f=0
state=0
utime.sleep(2)
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
    client = MQTTClient(CLIENT_ID, SERVER, PORT, USERNAME, PASSWORD)
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
        f=100
    elif k[0]=='lock':   
        f=1
        state=d["lock"]
    elif k[0]=='stop':   
        f=2
        state=d["stop"]
    elif k[0]=='up':   
        f=3
        state=d["up"]
    elif k[0]=='down':   
        f=4
        state=d["down"]
def subscribe(client):
    client.set_callback(on_message)
    client.subscribe(TOPIC1)

def main():
    global f
    do_connect()
    client= mqtt_connect()
    subscribe(client)
    while 1:
        if f==1:
            lock.value(state)
            utime.sleep(1)
            lock.value(0)
            msg_dict = {
                    'lock': 0
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print(1)
            f=0
        elif f==2:
            stop.value(state)
            utime.sleep(1)
            stop.value(0)
            msg_dict = {
                    'stop': 0
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print(2)
            f=0
        elif f==3:
            up.value(state)
            utime.sleep(1)
            up.value(0)
            msg_dict = {
                    'up': 0
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print(3)
            f=0
        elif f==4:
            down.value(state)
            utime.sleep(1)
            down.value(0)
            msg_dict = {
                    'down': 0
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print(4)
            f=0
        elif f==100:
            try:
                th.measure()
                t=th.temperature()
                h=th.humidity()
            except :
                print('TIMEDOUT')

            msg_dict = {
                    'temperature': t, 'humidity': h, 'person':person.value()
                }
            msg = ujson.dumps(msg_dict)
            result = client.publish(TOPIC, msg)
            print("Send '{msg}' to topic '{topic}'".format(msg = msg, topic = TOPIC))
            print(100)
            f=0
        elif f==0:
            client.check_msg()
            client.ping()
            utime.sleep_ms(200)

if __name__=='__main__':
    main()
