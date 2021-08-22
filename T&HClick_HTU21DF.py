from machine import I2C, Pin
import time
import os

device = 0x40
regAddresstemp = 0xE3
regAddresshum = 0xE5
TO_READ = 6
buff = bytearray(6)

class HTU21DF():
    def __init__(self,i2c,addr=device):
        self.addr = addr
        self.i2c = i2c
        b = bytearray(1) 
        b[0] = 0
        self.i2c.writeto_mem(self.addr,0xE6,b) #0x2d is POWER_CTL register
        b[0] = 16
        self.i2c.writeto_mem(self.addr,0xE6,b) #0x2d is POWER_CTL register
        b[0] = 8
        self.i2c.writeto_mem(self.addr,0xE6,b) #0x2d is POWER_CTL register
        
    def temperature(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddresstemp,TO_READ)
        temp=(buff[0] << 8) + buff[0]
        return -46.85 + (175.72 * temp / 65536)
    
    def humidity(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddresshum,TO_READ)
        hum=(buff[0] << 8) + buff[0]
        return -6 + (125.0 * hum/ 65536)
    
i2c = I2C("I2C_0")
tandh=HTU21DF(i2c)
while True:
    t=tandh.temperature()
    h=tandh.humidity()
    print("HUMIDITY = %d rh \t TEMPERATURE = %d °C" % (h,t))
    

