# -*- coding: utf-8 -*-
from machine import Pin,I2C
import machine
import utime
import onewire
from ds18x20 import DS18X20

OneWirePin = 15

def readDS18x20(): 
    # the device is on GPIO22
    dat = Pin(OneWirePin)
    # create the onewire object
    ds = DS18X20(onewire.OneWire(dat))
    # scan for devices on the bus
    roms = ds.scan()# 扫描挂载在单总线上的ds18B20设备
    ds.convert_temp() # 数据转换
    utime.sleep_ms(750)
    values = []   

    for rom in roms:
        values.append(ds.read_temp(rom))
        
    # values.append(u"℃")
#     print(values,r"℃")
    return values

def test():
	while 1:
		print(readDS18x20()[0])
		utime.sleep(5)		

if __name__=='__main__':
    test()