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

serial = i2c(port=1, address=0x3C)
device = hs1106(serial, rotate=1)
"""

from demo_opts import get_device
from PIL import Image,ImageOps
from turtle_pil import *


eyes=0
device=0
mood=0
sblink=0

alist = ['smile','angry','neutral','suprise']

def flatoval(r):               # Horizontal Oval
    right(45)
    for loop in range(2):
        circle(r,90)
        circle(r/2,90)

  

def eye(x, rad, m, z, ne):     # draw eyes (loc, size, pupil)
    home()
    goto(x, 20)
    down()
    circle(rad)
    
    if sblink==1 :
         up()           
         goto(x+rad,20+rad)    
         left(180)
         down()
         fd(2*rad)
         up()   
         return   
         
    if (ne==0): # no eyelids is false
        up()
        goto(x+rad,20+rad)
        left(147)
        circle(45,50)
    
    up()
    goto(x + eyes, 20+m)
    dot(z, "black")  #draw pupil
 
def mouth(m,a) :    # draw mouth (m=1,smile, m=2 straight, m=3 frown m=4 agape)
    home()
                  
    if m==1 :
        goto(-40, -10)
        down()
        right(90)
        circle(40, a)
    elif m==2:
        goto(-40, -10) 
        down()  
        fd(80)     
    elif m==3:
        goto(-40, -40)
        down()
        left(90)
        circle(-40, a)
    elif m==4:
        goto(-a/2, -40)
        down()
        flatoval(a)
                               
def draw_face() :
    # function for creation of the face
    global eyes,sblink, device
    
    if device == 0 :
        device = get_device()  
        print (device.width,device.height,device.mode)
        
    #print("face: ",alist[mood-1],mood, sblink)
    reset(128)                  
    penup()   
     
    if mood==1 : #happy
        eye(40, 20, 20,5,0)      
        eye(-40,20, 20,5,0)     
        mouth(1,180)          

    elif mood==2 : #angry
        eye(40, 20, 10, 5,0)     
        eye(-40,20, 10, 5,0)     
        mouth(3,180)          

    elif mood==3 :  #neutral
        eye(40, 20, 15, 10,0)      
        eye(-40,20, 15, 10,0)     
        mouth(2,120)          

    elif mood==4 :    #suprise
        eye(40, 20, 10, 10,1)      
        eye(-40,20, 10, 10,1)    
        mouth(4,20)                 
    
    done()
    
    img = Image.open("output.png")    
    img = img.resize((device.width, device.height), Image.BILINEAR).convert(device.mode)
    img = ImageOps.invert(img)
    device.display(img)
     

