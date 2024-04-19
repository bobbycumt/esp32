# -*- coding: utf-8 -*-
from machine import Pin,I2C
import utime
from lib import urequests
import ujson
import ssd1306

i2c=I2C(sda=Pin(21),scl=Pin(22))
display=ssd1306.SSD1306_I2C(128,32,i2c)
display.font_load("GB2312-12.fon")

ssid='bbhh'
psw='lb19850922'
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
def main():
    do_connect()
    place=input("请输入一个城市(拼音):")
    day=input("请输入一个日期选项:今天(0),明天(1),后天(2)")
    url="https://api.seniverse.com/v3/weather/daily.json?key=SzfBjdHiM0A3tzyhb&location="+place+"&language=zh-Hans&unit=c&start=0&"+day
    res=''
    respons=urequests.get(url)
    data=respons.text
    weather=ujson.loads(data)
#     print(weather['results'][0]['location']['name'],end='')
    if int(day)==0:
        res=weather['results'][0]['location']['name']+'今天'+'白天'+weather['results'][0]['daily'][0]['text_day']
        res1='晚上'+weather['results'][0]['daily'][0]['text_night']
        res2='气温'+weather['results'][0]['daily'][0]['low']+'到'+weather['results'][0]['daily'][0]['high']+'度'
        res3=weather['results'][0]['daily'][0]['wind_direction']+'风'+weather['results'][0]['daily'][0]['wind_scale']+'级'+'，湿度'+weather['results'][0]['daily'][0]['humidity']+'%'
    elif int(day)==1:
        res=weather['results'][0]['location']['name']+'明天'+'白天'+weather['results'][0]['daily'][0]['text_day']
        res1='晚上'+weather['results'][0]['daily'][0]['text_night']
        res2='气温'+weather['results'][0]['daily'][0]['low']+'到'+weather['results'][0]['daily'][0]['high']+'度'
        res3=weather['results'][0]['daily'][0]['wind_direction']+'风'+weather['results'][0]['daily'][0]['wind_scale']+'级'+'，湿度'+weather['results'][0]['daily'][0]['humidity']+'%'
    elif int(day)==2:
        res=weather['results'][0]['location']['name']+'后天'+'白天'+weather['results'][0]['daily'][0]['text_day']
        res1='晚上'+weather['results'][0]['daily'][0]['text_night']
        res2='气温'+weather['results'][0]['daily'][0]['low']+'到'+weather['results'][0]['daily'][0]['high']+'度'
        res3=weather['results'][0]['daily'][0]['wind_direction']+'风'+weather['results'][0]['daily'][0]['wind_scale']+'级'+'，湿度'+weather['results'][0]['daily'][0]['humidity']+'%'
    print(res+res1+res2+res3)
    for i in range(3):
        display.fill(0)
        display.text(res,0,0)
        display.text(res1,0,15)
        display.show() 
        utime.sleep(3)
        display.fill(0)
        display.text(res2,0,0)
        display.text(res3,0,15)
        display.show()
        utime.sleep(3)
if __name__=='__main__':
    main()