import RPi.GPIO as GPIO
import time
import sys

ERROR = 0xFE
PIN =  23
KEY = 0

State=0  # IDLE=0, START=1, REC=2 

timer=0
bits=0
bn=0
bytes=[0,0,0,0]
IRData=0
IRReady=False

log=[]

def between(a,b,c) :
    if a>=b and a<= c :
      return True
    else :
      return False

       
def ircheck(channel) :
    global State, timer, bits, bytes, bn, IRData, IRReady         

    tmp=time.time()
    pw = tmp - timer
    timer = tmp
    log.append(format(pw,'.4f'))
    
        
    if State == 0 :
      State = 1
      log.append("state 0")
      return
       
    elif State == 1 :

      if between(pw, 0.004, 0.008) :
          log.append("state 1")
          bits=0
          bn=0
          bytes=[0,0,0,0]
          State = 2
      else:
          #print(format(pw,'.4f'))
          State = 0
    
    elif State == 2 :            
      log.append("state 2")
      if not between(pw, 0.0007, 0.0026) :
          print(bn,pw)
          State = 0
          return
         
      if pw < 0.0012  :
        bytes[bn] = bytes[bn] >> 1
      else   :
        bytes[bn] = (bytes[bn] >> 1 ) | 0x80     
       
      bits += 1
      
      if bits == 8 :
       bits =0
       bn += 1
       if bn == 4 :
         State = 0  
         IRData=bytes 
         IRReady=True  
         log.append("ready ")
         log.append(IRData)         #print("ready", IRData)        
      
    
def clean():
    f=sys.stdout
    sys.stout=open("log.txt","w")
    print("irc log")
    print(log)
    sys.stdout.close()
    sys.stdout=f
    
    
def setup() :
    global IRReady, IRData

    GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
    
    GPIO.add_event_detect(PIN, GPIO.FALLING, 
        callback=ircheck) #, bouncetime=1)
        
    
def getKey():
    global IRReady, IRData
    
    if not IRReady :
      return ERROR
    IRReady = False
    return IRData[3]
    
    

    
if __name__ == '__main__':
# Use like this
    
  print('IR Remote Test  ...')
  setup()
  try:
      while True:
          key = getKey();
          if(key != ERROR):
              print("Get the key: 0x%02x" %key)
  except KeyboardInterrupt:
      clean()

