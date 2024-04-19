import time
from machine import Pin
def main():
    led=Pin(12,Pin.OUT)
    while 1:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
    
if __name__ == '__main__':
    main()