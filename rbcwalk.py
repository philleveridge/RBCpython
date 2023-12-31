
import time as tim
import wckmodule as wm
import wckplay as wp
import wckkey as kb
        
##################################

import math

a=[10,13,15,11,10,10,13,15,11,10,22,1,9,22,1,9]
b=[122,166,210,92,107,129,83,42,159,144,91,43,50,161,209,205]
c=[0,2,8,5,0,15,2,8,6,15,5,11,5,5,5,5]

wm.connect()

input ("ready to stand")

wp.standup(16)

input ("press any key to start walk")

Speed=16
NoS=16

with kb.KeyBoard() as ky:
	i = 0
	k=0

	noquit=True

	while noquit:
		i= i + 1

		for x in range(Speed) :
			print (x, " ",end='')
			p=[]
			k = ky.get_key()

			if k == '\x1b' or k=='q' : # x1b is ESC
				noquit=False
				break
				
			if k=="f" :
			    Speed -= 2
			if k=="s" :
			    Speed += 2

			for y in range(NoS) :			
				p.append(int(b[y]+a[y]*math.sin((x+c[y])*3.1415*2.0/Speed  ) ))  # calculate the Sine wave offset
								
			print(p,".")
			wp.PlayPose(25, 1, 4, p, 16)

print("done")		
wp.standup(16)

	
	
	###eg data

#0  [122, 175, 210, 102, 107, 125, 92, 42, 166, 140, 111, 42, 58, 181, 209, 213] .
#1  [125, 178, 204, 99, 110, 128, 95, 36, 163, 143, 106, 42, 56, 176, 209, 211] .
#2  [129, 178, 199, 96, 114, 132, 95, 31, 159, 147, 99, 42, 53, 169, 209, 208] .
#3  [131, 178, 196, 92, 116, 136, 95, 28, 154, 151, 91, 42, 50, 161, 209, 205] .
#4  [131, 175, 195, 87, 116, 138, 92, 27, 151, 153, 82, 42, 46, 152, 208, 201] .
#5  [131, 170, 196, 84, 116, 138, 87, 28, 148, 153, 75, 42, 43, 145, 208, 198] .
#6  [129, 166, 199, 81, 114, 138, 83, 31, 148, 153, 70, 43, 41, 140, 208, 196] .
#7  [125, 161, 204, 81, 110, 136, 78, 36, 148, 151, 69, 43, 41, 139, 208, 196] .
#8  [122, 156, 209, 81, 107, 132, 73, 41, 151, 147, 70, 43, 41, 140, 208, 196] .
#9  [118, 153, 215, 84, 103, 129, 70, 47, 154, 144, 75, 43, 43, 145, 208, 198] .
#10  [114, 153, 220, 87, 99, 125, 70, 52, 158, 140, 82, 43, 46, 152, 208, 201] .
#11  [112, 153, 223, 91, 97, 121, 70, 55, 163, 136, 90, 43, 49, 160, 208, 204] .
#12  [112, 156, 224, 96, 97, 119, 73, 56, 166, 134, 99, 43, 53, 169, 209, 208] .
#13  [112, 161, 223, 99, 97, 119, 78, 55, 169, 134, 106, 43, 56, 176, 209, 211] .
#14  [114, 165, 220, 102, 99, 119, 82, 52, 169, 134, 111, 42, 58, 181, 209, 213] .
#15  [118, 170, 215, 102, 103, 121, 87, 47, 169, 136, 112, 42, 58, 182, 209, 213] .


