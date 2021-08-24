import time,utime
from machine import Pin


LED = Pin(("GPIO_0", 30), Pin.OUT)
while True:
    LED.value(1)
    utime.sleep_ms(1)
    LED.value(0)
    utime.sleep_ms(1)