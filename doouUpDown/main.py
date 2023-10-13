import machine
import mixiot
from ubinascii import hexlify
import time

def m1(client, topic, msg):
    if int(msg) == 1:
        up.value(1)
        time.sleep_ms(500)
        up.value(0)
    else:
        up.value(0)

def m2(client, topic, msg):
    if int(msg) == 1:
        down.value(1)
        time.sleep_ms(500)
        down.value(0)
    else:
        down.value(0)

def m3(client, topic, msg):
    if int(msg) == 1:
        lock.value(1)
        time.sleep_ms(500)
        lock.value(0)
    else:
        lock.value(0)

def m4(client, topic, msg):
    if int(msg) == 1:
        stop.value(1)
        time.sleep_ms(500)
        stop.value(0)
    else:
        stop.value(0)



up = machine.Pin(15, machine.Pin.OUT)
down = machine.Pin(4, machine.Pin.OUT)
lock = machine.Pin(2, machine.Pin.OUT)
stop = machine.Pin(5, machine.Pin.OUT)
mixiot.wlan_connect('CU_future','13582579999')
MQTT_USR_PRJ = 'bobbycumt@163.com/test/'
mqtt_client = mixiot.init_MQTT_client('mixio.mixly.cn', 'bobbycumt@163.com', '500f0e0c7110446a2320bd5eb652f447', MQTT_USR_PRJ)
mqtt_client.set_callback('up',m1, MQTT_USR_PRJ)
mqtt_client.subscribe(MQTT_USR_PRJ + 'up')
mqtt_client.set_callback('down',m2, MQTT_USR_PRJ)
mqtt_client.subscribe(MQTT_USR_PRJ + 'down')
mqtt_client.set_callback('lock',m3, MQTT_USR_PRJ)
mqtt_client.subscribe(MQTT_USR_PRJ + 'lock')
mqtt_client.set_callback('stop',m4, MQTT_USR_PRJ)
mqtt_client.subscribe(MQTT_USR_PRJ + 'stop')
while True:
    mqtt_client.check_msg()
