import smbus
import time

import RPi.GPIO as gpio


class MPU6050(object):

  global PWR_M
  global DIV
  global CONFIG
  global GYRO_CONFIG
  global INT_EN
  global ACCEL_X 
  global ACCEL_Y
  global ACCEL_Z
  global GYRO_X
  global GYRO_Y
  global GYRO_Z
  global TEMP
  
  global RS
  global EN
  global D4
  global D5
  global D6
  global D7   
  global Device_Address  # device address
  
  PWR_M   = 0x6B
  DIV   = 0x19
  CONFIG       = 0x1A
  GYRO_CONFIG  = 0x1B
  INT_EN   = 0x38
  ACCEL_X = 0x3B
  ACCEL_Y = 0x3D
  ACCEL_Z = 0x3F
  GYRO_X  = 0x43
  GYRO_Y  = 0x45
  GYRO_Z  = 0x47
  TEMP = 0x41
  
  RS =18
  EN =23
  D4 =24
  D5 =25
  D6 =8
  D7 =7
   
  Device_Address = 0x68   # device address
  
  AxCal=0
  AyCal=0
  AzCal=0
  GxCal=0
  GyCal=0
  GzCal=0
  
  bus=0
    
  def __init__(self):    
    self.bus = smbus.SMBus(1)
    
    gpio.setup(RS, gpio.OUT)
    gpio.setup(EN, gpio.OUT)
    gpio.setup(D4, gpio.OUT)
    gpio.setup(D5, gpio.OUT)
    gpio.setup(D6, gpio.OUT)
    gpio.setup(D7, gpio.OUT)
    
    self.begin();
    self.InitMPU()
    self.calibrate()
  
  def begin(self): 
    self.cmd(0x33) 
    self.cmd(0x32) 
    self.cmd(0x06)
    self.cmd(0x0C) 
    self.cmd(0x28) 
    self.cmd(0x01) 
    time.sleep(0.0005)   
  
  def cmd(self,ch): 
    gpio.output(RS, 0)
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
  
    if ch&0x10==0x10:
      gpio.output(D4, 1)
  
    if ch&0x20==0x20:
      gpio.output(D5, 1)
  
    if ch&0x40==0x40:
      gpio.output(D6, 1)
  
    if ch&0x80==0x80:
      gpio.output(D7, 1)
  
    gpio.output(EN, 1)
    time.sleep(0.005)
  
    gpio.output(EN, 0)
  
    # Low bits
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
  
    if ch&0x01==0x01:
      gpio.output(D4, 1)
  
    if ch&0x02==0x02:
      gpio.output(D5, 1)
  
    if ch&0x04==0x04:
      gpio.output(D6, 1)
  
    if ch&0x08==0x08:
      gpio.output(D7, 1)
  
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)
  
  def write(self,ch): 
    gpio.output(RS, 1)
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
  
    if ch&0x10==0x10:
      gpio.output(D4, 1)
  
    if ch&0x20==0x20:
      gpio.output(D5, 1)
  
    if ch&0x40==0x40:
      gpio.output(D6, 1)
  
    if ch&0x80==0x80:
      gpio.output(D7, 1)
  
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)
  
    # Low bits
  
    gpio.output(D4, 0)
    gpio.output(D5, 0)
    gpio.output(D6, 0)
    gpio.output(D7, 0)
  
    if ch&0x01==0x01:
      gpio.output(D4, 1)
  
    if ch&0x02==0x02:
      gpio.output(D5, 1)
  
    if ch&0x04==0x04:
      gpio.output(D6, 1)
  
    if ch&0x08==0x08:
      gpio.output(D7, 1)
  
    gpio.output(EN, 1)
    time.sleep(0.005)
    gpio.output(EN, 0)
  
  
  def InitMPU(self):
  	self.bus.write_byte_data(Device_Address, DIV, 7)
  	self.bus.write_byte_data(Device_Address, PWR_M, 1)
  	self.bus.write_byte_data(Device_Address, CONFIG, 0)
  	self.bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
  	self.bus.write_byte_data(Device_Address, INT_EN, 1)
  	time.sleep(1)
  
  
  def readMPU(self,addr):
  	high = self.bus.read_byte_data(Device_Address, addr)
  	low = self.bus.read_byte_data(Device_Address, addr+1)
  	value = ((high << 8) | low)
  
  	if(value > 32768):
  		value = value - 65536
  
  	return value
  
  def accel(self):
    x = self.readMPU(ACCEL_X)
    y = self.readMPU(ACCEL_Y)
    z = self.readMPU(ACCEL_Z)
    
    Ax = (x/16384.0-self.AxCal) 
    Ay = (y/16384.0-self.AyCal) 
    Az = (z/16384.0-self.AzCal)
    
    return Ax,Ay,Az
  
  def gyro(self):
    global GxCal
    global GyCalpython
    global GzCal
  
    x = self.readMPU(GYRO_X)
    y = self.readMPU(GYRO_Y)
    z = self.readMPU(GYRO_Z)
    Gx = x/131.0 - self.GxCal
    Gy = y/131.0 - self.GyCal
    Gz = z/131.0 - self.GzCal
  
    return Gx,Gy,Gz
  
  
  def temp(self):
    tempRow=self.readMPU(TEMP)
    tempC=(tempRow / 340.0) + 36.53
    tempC="%.2f" %tempC
    return  tempC
  
  
  def calibrate(self):
    x=0
    y=0
    z=0
  
    for i in range(50):
        x = x + self.readMPU(ACCEL_X)
        y = y + self.readMPU(ACCEL_Y)
        z = z + self.readMPU(ACCEL_Z)
  
    x= x/50
    y= y/50
    z= z/50
  
    self.AxCal = x/16384.0
    self.AyCal = y/16384.0
    self.AzCal = z/16384.0
  
    x=0
    y=0
    z=0
  
    for i in range(50):
      x = x + self.readMPU(GYRO_X)
      y = y + self.readMPU(GYRO_Y)
      z = z + self.readMPU(GYRO_Z)
  
    x= x/50
    y= y/50
    z= z/50
  
    self.GxCal = x/131.0
    self.GyCal = y/131.0
    self.GzCal = z/131.0


if __name__ == '__main__':
# Use like this 
    print("Test MPU6050 Interface")
    
    mpu=MPU6050()
    
    while 1: 
      print("Accel --  Gyro")    
      for i in range(30):
        a,b,c=mpu.accel()
        d,e,f=mpu.gyro()      
        print ("{0} {1:.2f},{2:.2f}{3:.2f} -- {4:.2f},{4:.2f},{6:.2f}".format(i,a,b,c,d,e,f))
        time.sleep(1)

