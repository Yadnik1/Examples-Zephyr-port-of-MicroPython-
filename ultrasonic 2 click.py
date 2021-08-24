from machine import UART,Pin
import time,utime
import sys

buf0 = b'\x55\x00\x01\xFE'
buf1 = b'\x55\x01\x01\xFD'
buf5= b'\x55\x05\xFA'
buf10=b'\x55\x0A\x26\x00\xCF'
buf17=b'\x55\x11\x01\xED'
buf19 =b'\x55\x13\x01\xEB'
buf25 = b'\x55\x19\x88\x88\x88\x88\x88\x88b\x84\x21\x08\x42b\x10\x80\x80\x80\x80\x00\x88\x88\x88\x88\x88\x88\x84\x21\x08\x42\x10\x80\x80\x80\x80\x00\x7C'


class Ultrsonic:

    def __init__(self,uart):
        self.uart = uart

    def distance_mm(self):
            
            utime.sleep_ms(1)
            uart.write(buf25)
            utime.sleep_ms(1)
            uart.write(buf10)
            utime.sleep_ms(1)
            t = 0
            buf = bytearray(2)
            while t < 1000:
                t = t + 1
                utime.sleep_ms(5)
            if t < 1000:
                uart.readinto(buf, 2)           
            dist = buf[0] * 256 + buf[1]
            if dist > 1100:
                    dist = -1                
            return(dist)
            utime.sleep_ms(1)
            uart.write(buf17)
            utime.sleep_ms(1)
            uart.write(buf5)
            utime.sleep_ms(1)

uart=UART("UART_1")
sonar=Ultrsonic(uart)
while True:
    obstacle_distance=sonar.distance_mm()
    print(obstacle_distance)

    
