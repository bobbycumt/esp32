import machine as mc
import time
import network
import urequests
import ujson
import ssd1306

ssid = 'bbhh'
password = 'lb19850922'
key = 'Si6TGH32UBUyOOWjZ'
#四个城市：唐山、延安、哈尔滨、海口
city1 = 'tangshan'
city2 = 'yanan'
city3 = 'haerbin'
city4 = 'haikou'
url_f = 'https://api.seniverse.com/v3/weather/now.json?key='
url_m = '&location='
url_b = '&language=zh-Hans&unit=c'
#led连接到了2号引脚
led = mc.Pin(2,mc.Pin.OUT)
#按钮连接到了0号引脚
btn = mc.Pin(0,mc.Pin.IN)

#OLED初始化
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

#wifi连接函数
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
#打印hello world后led以1Hz频率闪烁
#按下按钮后退出程序
def main():
    OLEDInit()
    print("hello world!")
    do_connect()    
    oled.show()
    oled.invert(False) 

    while(1):
        response = urequests.get(url_f+key+url_m+city1+url_b)
        j1=ujson.loads(response.text)
        print(j1['results'][0]['location']['name'],end='\n')
        print(j1['results'][0]['now']['text'],end='\n')
        print(j1['results'][0]['now']['temperature'],end='`C\n')
        print(j1['results'][0]['last_update'])
        oled.fill(0)
        oled.text('ThinkBob', 30, 5)
        oled.text(' tangshan:'+j1['results'][0]['now']['temperature']+'`C',5,20)
        oled.show()

        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(5)

        response = urequests.get(url_f+key+url_m+city2+url_b)
        j2=ujson.loads(response.text)
        print(j2['results'][0]['location']['name'],end='\n')
        print(j2['results'][0]['now']['text'],end='\n')
        print(j2['results'][0]['now']['temperature'],end='`C\n')
        print(j2['results'][0]['last_update'])
        
        oled.text(' yanan:'+j2['results'][0]['now']['temperature']+'`C',5,30)
        oled.show()
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(5)

        response = urequests.get(url_f+key+url_m+city3+url_b)
        j3=ujson.loads(response.text)
        print(j3['results'][0]['location']['name'],end='\n')
        print(j3['results'][0]['now']['text'],end='\n')
        print(j3['results'][0]['now']['temperature'],end='`C\n')
        print(j3['results'][0]['last_update'])
        
        oled.text(' haerbin:'+j3['results'][0]['now']['temperature']+'`C',5,40)
        oled.show()
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(5)

        response = urequests.get(url_f+key+url_m+city4+url_b)
        j4=ujson.loads(response.text)
        print(j4['results'][0]['location']['name'],end='\n')
        print(j4['results'][0]['now']['text'],end='\n')
        print(j4['results'][0]['now']['temperature'],end='`C\n')
        print(j4['results'][0]['last_update'])
        
        oled.text(' haikou:'+j4['results'][0]['now']['temperature']+'`C',5,50)
        oled.show()
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(600)

        
        if btn.value()==0:
            break
if __name__ == '__main__':
    main()