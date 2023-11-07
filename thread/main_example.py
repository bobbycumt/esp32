from umqtt.simple import MQTTClient
from machine import Pin
import network
import utime
import random
import ujson
import _thread

f=0
wlan = network.WLAN(network.STA_IF)
up = Pin(15, Pin.OUT)
down = Pin(4, Pin.OUT)
lock = Pin(2, Pin.OUT)
stop = Pin(5, Pin.OUT)

# ssid = 'CU_future'
# password = '13582579999'
ssid = 'bbhh'
password = 'lb19850922'

client_id='pc_esp32' 
server = 'bj-2-mqtt.iot-api.com' 
port = 1883 #连接的端口
user = 'gi9ruf6zithfmw64' #产品的数字ID
pwd = 'VW6nAnxPSC'

# Received messages from subscriptions will be delivered to this callback
c = MQTTClient(client_id, server,port,user,pwd,60)  
gLock = None 

def sub_cb(topic, msg):
    # print((topic, msg))
    msg=ujson.loads(msg)
    # print(list(msg.keys())[0])
    if list(msg.keys())[0]=='lock':
        lock.value(int(msg['lock']))
        utime.sleep(1)
        lock.value(0)
    if list(msg.keys())[0]=='stop':
        stop.value(int(msg['stop']))
        utime.sleep(1)
        stop.value(0)
    if list(msg.keys())[0]=='up':
        up.value(int(msg['up']))
        utime.sleep(1)
        up.value(0)
    if list(msg.keys())[0]=='down':
        down.value(int(msg['down']))
        utime.sleep(1)
        down.value(0) 
def do_connect():
#     wlan = network.WLAN(network.STA_IF)
    
    wlan.active(False)
    utime.sleep_ms(100)
    wlan.active(True)
    # print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def wifi_con():
    print('----1----')
    global f
    while 1:
        if not wlan.isconnected():
            wlan.active(False)
            utime.sleep_ms(100)
            wlan.active(True)
            print('connecting to network...')
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                pass
            print('network config:', wlan.ifconfig())
            c.set_callback(sub_cb)
            c.connect()
            c.subscribe("attributes/push")  
            f=1    

def chkmsg():
    print('----2----')
    while 1:
        c.wait_msg()
    
def online():
    print('----3----')
    while 1:
        c.ping()
        utime.sleep(10)
        print("online")

def main():
    global f
    print('----所有线程开始执行----')
    #创建互斥锁
    gLock = _thread.allocate_lock()
    
    #获得互斥锁
    gLock.acquire()
    
    #创建线程1
    _thread.start_new_thread(wifi_con,())
    while 1:
        if f:
            f=0
            _thread.start_new_thread(chkmsg,())
            _thread.start_new_thread(online,())
    #休眠
    # utime.sleep(5)
    
    #释放互斥锁
    # gLock.release()
    
    # print('----主程序正在执行----')
    # led.value(0)
if __name__=='__main__':
     main()