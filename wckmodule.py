#
# Robobuilder WcK module library
import serial

import time as tim

f=0
dbg=0

def connect(sp="") :
    "connect to serial port"
    global f
    if sp=="" :
        sp="/dev/ttyUSB0"
    
    #sp="/dev/rfcomm0"
    try :
        f = serial.Serial(sp, baudrate=115200, timeout=0.5)
        print ('connected to ',sp)
        f.write(b'MM')  # force to DCMP mode (just in in basic)
        f.flush()
    except :
        print ('Failed to connect to ',sp)   
        
         
def writeByte(b) :
    "write byte to wck servo"
    global f
    
    if f==0 : return 0
    
    if isinstance(b,int) : 
        print ("int",b)
        f.write(b)

    if isinstance(b,bytearray) : 
        f.write(b)    
        f.flush()
     
    return

def readByte() :
    "read byte from wck servo"
    global f
    
    if f==0 : return 0
        
    a=f.read(1)
    return a
    
def readWord() :
    "read byte from wck servo"
    global f
    
    if f==0 : return (-1,-1)
    
    a=f.read(2)
    try :
        return (a[0],a[1])
    except :
        return (-1,-1)

def SendOperCommand(Data1,Data2) :
    "sends a 4 byte packet broadcast to wck servos"
    chksum = (Data1 ^ Data2) & 0x7F
    ba = bytearray([0xFF,Data1,Data2,chksum])
    writeByte(ba)
    return 1
    
def SendSetCommand(ServoID, Data1, Data2, Data3) :
    "sends a 4 byte packet broadcast to wck servos"
    cmd = 0xE0|ServoID
    chksum = (cmd ^ Data1 ^ Data2 ^ Data3) & 0x7F
    ba = bytearray([0xFF,cmd, Data1, Data2, Data3, chksum])
    writeByte(ba)
    return 1    
    
def setPDgain(ServoID,PV,DV) :
    SendSetCommand(ServoID, 11, PV, DV)  # runtime = 11 / 9
    return readWord()
 
def setIgain(ServoID,IV) :
    SendSetCommand(ServoID, 24, IV, IV)  # runtime = 24 / 21
    return readWord()  
    
def setIO(ServoID,Data) :
    if (Data <0) or (Data>3) :
        print("Out of range")
        return (-1,-1)    
    SendSetCommand(ServoID, 100, Data, Data) 
    return readWord()       

def setSpeed(ServoID,Sp, Acc) :
    if (Sp<0) or (Sp>30) or (Acc<20) or (Acc>100) :
        print("Out of range")
        return (-1,-1)
    SendSetCommand(ServoID, 13, Sp, Acc)
    return readWord()    

def getPDgain(ServoID) :
    SendSetCommand(ServoID, 10, 0, 0)  #  
    return readWord()
 
def getIgain(ServoID) :
    SendSetCommand(ServoID, 22, 0, 0)  # 
    return readWord()  
    
def getIO(ServoID) :  
    SendSetCommand(ServoID, 101, 0, 0) 
    return readWord()       

def getSpeed(ServoID) :
    SendSetCommand(ServoID, 14, 0, 0)
    return readWord()  


def SyncPosSend(LastID, SpeedLevel, TargetArray, Index) :
    "sends a variable length packet to all servo in range"
    global f
    cs=0
    ba = bytearray(LastID+5)
    ba[0]=0xFF
    ba[1]=(SpeedLevel<<5)|0x1F
    ba[2]=LastID+1
    for i in range(0,LastID+1) :
        ba[i+3]=int(TargetArray[i+Index*(LastID+1)])
        cs = (cs ^ ba[i+3]) & 0xFF
    ba[LastID+4]= (cs & 0x7F)

    #print("dbg: ",list(ba))
    writeByte(ba)
    return 1

def setpassive(ServoID) :
    "sends Passive wCK Command to wCK module"
    SendOperCommand(0xc0|ServoID, 0x10)
    return readWord()


def getservo(ServoID) :
    "getservo values for ServoID. returns two bytes load and position"
    #print ("GET ",ServoID)
    SendOperCommand(0xA0|ServoID,0)
    return readWord()

    
def getspecial(cmd) :
    "get special"
    #print ("GET ",ServoID)
    SendOperCommand(0xA0|30,cmd)
    return readWord()

def setservo(ServoID,Torque,Position) :
    "set servo position and torque values"
    #print ("SET ",ServoID,"=",Position)
    SendOperCommand((Torque<<5)|ServoID,Position)
    r=readWord()
    if len(r)>1 :
        return r
    else :
        print ("? ",r)
        return (-1,-1)

def test(i):
    "test module"
    print ("Wck module test=%d" % i)
    connect()
    pos = getservo(i)
    for _ in range(5) :
        print (_)
        setservo(i,4,pos[1] + 5)
        tim.sleep(2)
        setservo(i,4,pos[1])
        tim.sleep(2)
        setservo(i,4,pos[1] - 5)
        tim.sleep(2)
        setservo(i,4,pos[1])
        tim.sleep(2)

 
import sys
if __name__ == "__main__":
    if len(sys.argv)>1 :
        test(int(sys.argv[1]))

    else :
        test(24)
