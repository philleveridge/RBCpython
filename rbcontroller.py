#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays an animated gif.

usage:

python faces.py --display=pygame
python faces.py --display=hs1106

"""

from time import sleep
import threading as th

import wckkey as kb
import wckplay as wp
import wckmodule as wm
import wckirc  as ir


import rbcfaces as rf
import rbcservos as rs
import rbcsdb as db

import math
    
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from mpu6050 import mpu6050
import wckirc as ir
import RPi.GPIO as GPIO


redLED=22
yellowLED=27
greenLED=17

lights=[redLED, yellowLED,  greenLED]

HALT=False

servo_list= []
initpos   = []

def heart_beat() :
    global mood,sblink
    while not HALT :
      GPIO.output([redLED, yellowLED],GPIO.HIGH)
      GPIO.output(greenLED,GPIO.LOW)
      
      sleep(1)
      
      GPIO.output([redLED, yellowLED],GPIO.LOW)
      GPIO.output(greenLED,GPIO.HIGH)
      
      sleep(1)
      
      GPIO.output([redLED, yellowLED],GPIO.HIGH)
      GPIO.output(greenLED,GPIO.LOW)
      
      sleep(1)
      
      GPIO.output([redLED, yellowLED],GPIO.LOW)
      GPIO.output(greenLED,GPIO.HIGH)
      
      rf.sblink=1
      rf.draw_face()
      sleep(0.5)
      rf.sblink=0 
      rf.draw_face() 
      sleep(0.5) 
        
    
            
def walkcont() :
    a=[10,13,15,11,10,10,13,15,11,10,22,1,9,22,1,9]
    b=[122,166,210,92,107,129,83,42,159,144,91,43,50,161,209,205]
    c=[0,2,8,5,0,15,2,8,6,15,5,11,5,5,5,5]

    input ("press any key to start walk")

    with kb.KeyBoard() as ky:
    
        Speed=16
        NoS=16
        i = 0
        k=0

        noquit=True

        while noquit:
            i= i + 1
            
            for x in range(Speed) :
                print (x, " ",end='')
                p=[]
                
                ch = ky.get_key()
                if ch != False and ch != "" :              
                    if (ch == '\x1b') or  (ch=='q') :
                        noquit=False
                        print("Quit");

                for y in range(NoS) :			
                    p.append(int(b[y]+a[y]*math.sin((x+c[y])*3.1415*2.0/Speed  ) ))  # calculate the Sine wave offset

                print(p,".")
                wp.PlayPose(25, 1, 4, p, 16)


    

def do_builtin(n) :
    print("do - ", n)
    if db.exists(n) :  
        if type(db.get(n)) is str :
            do_builtin(db.get(n))
        else : 
            if db.exists("+"+n) :
                rs.play(servo_list, move=db.get(n), extras=db.get("+"+n))   
            else :   
                rs.play(servo_list, move=db.get(n))    
            rf.mood=1
    else:
        print ("No such sequence")
        rf.mood=2
                   
def main_loop():   

    global servo_list
                        
    with kb.KeyBoard() as ky:
        print("Robobuilder Controller v0.1")   
        print ("\n:> ", end="")
        
        while True:

                        
            ch = ir.getKey();
            if ch != ir.ERROR :
                print("Get the ir: 0x%02x" %ch)
                
                if ch == 7:  # Red {}
                    print("stopped");
                    return
                    
                if (ch >= 12) and (ch <= 23) :
                    do_builtin(str(ch-11))
            
                                                 
            ch = ky.get_key()
            if ch != False and ch != "" :
                print(ch)         
            
                if (ch == '\x1b') or  (ch=='q') :
                    print("done");
                    return
                    
                if ch=='l' :
                    rf.eyes = -10

                if ch=='r' :
                    rf.eyes = 10
                    
                if ch=='n' :
                    rf.eyes = 0
                    
                if ch=='n' :
                    rf.mood = rf.mood +1
                    if rf.mood > 4 : rf.mood=1
                                                                                           
                if ch == 'a' :   
                    accel_data = mpu.get_accel_data() # [1,0,0] # 
                    gyro_data = mpu.get_gyro_data() # [0,0,1] #              
                    rs.record(servo_list, status=[1000, 2, rf.mood,rf.eyes, accel_data, gyro_data])                
                    db.insert("TEMP", rs.moves)
                    
                    
                if ch == 'b' :
                    rs.play(servo_list)
                    rs.passiv(servo_list)
                    rf.mood=1
                    
                if ch == 'c' :
                    rs.clr()
                    
                if ch == 'z' :
                    rs.querynset()
                    
                if ch == 'p' :
                    rs.passiv(servo_list)
                    rf.mood=4
                    
                if ch == 'f' :
                    (servo_list,initpos) = rs.find()
                    db.insert("SERVOS", servo_list)
                    db.insert("POS", initpos)
                    print("servos = ",servo_list)   
                    
                if ch == 'w' :
                    n=input("save word?")
                    print(n)
                    db.insert(n, rs.moves)
                    
                if ch == 's' :
                    n=input("save shortcut?")
                    print(n)
                    x=input("shortcut?")
                    if db.exists(x) :
                        db.insert(n, x)      
                    else :
                        print(f"Action '{x}' does not exist")          
                    
                if ch == 'x' :
                    n=input("word?")
                    do_builtin(n)     
                                   
                if ch == '?' :
                    print(rs.moves)
                    db.show()
                    
                if ((ch >= '0') and (ch <= '9')) or ((ch>= 'A') and (ch<='Z')) :
                    do_builtin(ch)   
                                               
                if (ch=='v') :
                    walkcont ()                 
                                        
                rf.draw_face ()
                sleep(0.1)
                print ("\n:> ", end="")



def servolistchk(a,b) : #a=servo_list, b=database
    if (a==b) : return True
    for i in range (0,len(a)) :
        if i==len(b):
            return True  
        if a[i] != b[i] :
            return False       
    return True 
 
 
import sys, getopt
       
def main(argv) :
    global lights
    conn=""
    dbname="rbcontroller.txt"
    pf=True
         
    opts, args = getopt.getopt(argv,"hb:t:",["dbfile=", "tty="])
    for opt, arg in opts:
        if opt == '-h':
            print ('rbcontroller.py -b <dbname> -t <tty>')
            sys.exit()
        elif opt in ("-b"):
            dbname = arg    
            pf=False
        elif opt in ("-t"):
            conn = arg  
                
    wm.connect(sp=conn)
    
    if (pf==False) or (input("Load db " + dbname + " ?")=="y") :
        db.load(dbname)
        rs.moves=db.get("TEMP")
    else :
        db.clear(dbname)
        db.insert("VER", "1")   
        
    
    ir.setup()
    GPIO.setup(lights, GPIO.OUT) # set a port/pin as an output
            
    return

                                
if __name__ == "__main__":

    try: 
      main(sys.argv[2:])
      sys.argv=sys.argv[0:2]   
      
      rf.mood=1
      rf.draw_face ()
      
      (servo_list, initpos) = rs.find()
      print("servos = ",servo_list)
      
      if not servolistchk(servo_list,db.get("SERVOS")) :
        print("? Error database servo list does not match current servos found")
        db.clear()
      
      db.insert("SERVOS", servo_list)
      db.insert("POS", initpos)
      
      
      mpu = mpu6050(0x68)    
      S = th.Timer(1.0, heart_beat) 
      S.start()
      
      main_loop()
      HALT=True
      if input("Save db?")=="y" :
        db.store()
      else :
        print("Not saved")
        
      ir.clean()
            
    except KeyboardInterrupt:
        pass


