#
#Python module to play poses

import time
import wckmodule as wck

nos       = 16
#enum { AccelDecel=0, Accel, Decel, Linear };
AccelDecel= 0
Accel     = 1
Decel     = 2 
Linear    = 3


cpos      = list(range(32))
initpos   = list(range(32))

# ServoID      0 , 1 , 2, 3 , 4 , 5, 6 ,7 , 8 ,9 ,10,11,12,13, 14, 15 
basic16   = [125,179,199,88,108,126,72,49,163,141,51,47,49,199,205,205]
ibp       = 0

def delay_ms(tm) :
    "milisecond time delay"
    time.sleep(tm/1000.0)

##########################################
#
# Play d ms per step, f frames, from current -> spod
#
##########################################
def PlayPose(d, f, tq, spod, flag) :
    "Send a sequence of 'f' moves to go from starting position to final position in a number of step of total duration d (ms)"
    global cpos,nos
    if (flag!=0) :
        readservos(0)  #set nos and reads cpos
        flag=nos
    dur=d/f
    if (dur<25) : dur=25 #25ms is quickest
    temp=list(range(nos))
    for i in range(f) :
        for j in range(nos) :
            temp[j] = round(GetMoveValue(PP_mtype, cpos[j], spod[j], float(i+1) / f))
        wck.SyncPosSend(nos-1, tq, temp, 0)
        delay_ms(dur)

    for i in range(nos) :
        cpos[i]=spod[i]
    #wck.SyncPosSend(nos-1, tq, cpos, 0)
    delay_ms(dur)

##########################################
#
##########################################
def initbp(n) :
    "initial basic position and set global flag when done"
    global ibp
    nw = n%32
    for j in range(nw) :
        if (nw<=16) :
            initpos[j]=basic16[j]
        else :
            if (dm) :
                initpos[j]=basicdh[j]  # dance hands
            else :
                initpos[j]=basic18[j]
        ibp=1

##########################################
#
##########################################
def initbpfromcpos() :
    "initialise basic position using current position"
    global nos,ibp,cpos,initpos
    nw=nos

    if (nw<16 or nw>24)  :
        print ("?err=", nw)
        return

    for j in range (nw) :
        initpos[j]=cpos[j]
    ibp=1

##########################################
#
##########################################
def standup (n) :
    "stand up. n defines number of servos i.e. 16 in standard model"
    global ibp,initpos
    nw = n%32
    if (not ibp) :
        initbp(nw)
    PlayPose(1000, 10, 4, initpos, nw) #huno basic


##########################################
#
##########################################
def readservos(n) :
    "read all servos into current position array"
    global nos,cpos

    if n==0 :
    	n=16

    for i in range(n) : 
        _,p = wck.getservo(i)
        if (p<0 or p>255) :
            print (p," break")
        cpos[i]=int(p)
    nos=n
    return n

##########################################
#
##########################################
def passiveservos(n=16) :        
    "set servos to passive mode - so they can be manually positioned"

    for i in range(n) : 
        _,p = wck.setpassive(i)
        if (p<0 or p>255) : break
    return i

##########################################
#
# Different type of move interpolation
# from http://robosavvy.com/forum/viewtopic.php?t=5306&start=30
# original by RN1AsOf091407
#
##########################################

PP_mtype=Linear

##########################################
#
##########################################
def CalculatePos_Accel(Distance, FractionOfMove) :
    return FractionOfMove * (Distance * FractionOfMove)

##########################################
#
##########################################
def CalculatePos_Decel(Distance, FractionOfMove) :
    FractionOfMove = 1 - FractionOfMove
    return Distance - (FractionOfMove * (Distance * FractionOfMove))

##########################################
#
##########################################
def CalculatePos_Linear(Distance, FractionOfMove) :
    return (Distance * FractionOfMove)

##########################################
#
##########################################
def CalculatePos_AccelDecel(Distance, FractionOfMove) :
    if ( FractionOfMove < 0.5 ) :    # Accel:
        return CalculatePos_Accel(Distance /2, FractionOfMove * 2);
    elif (FractionOfMove > 0.5 ) : # Decel:
        return CalculatePos_Decel(Distance/2, (FractionOfMove - 0.5) * 2) + (Distance * 0.5)
    else :                           # = .5! Exact Middle.
        return Distance / 2

##########################################
#
##########################################
def GetMoveValue(mt, StartPos, EndPos, FractionOfMove) :
    "calculates the amount to move each servo depending on type of interpolation required. Linear is most basic, i.e. same amount in each step"
    Offset=0
    Distance=0
    
    if (StartPos > EndPos) :
        Distance = StartPos - EndPos
        Offset = EndPos
        if mt == Accel:
            return Distance - CalculatePos_Accel(Distance, FractionOfMove) + Offset
        elif mt== AccelDecel:
            return Distance - CalculatePos_AccelDecel(Distance, FractionOfMove) + Offset
        elif mt== Decel:
            return Distance - CalculatePos_Decel(Distance, FractionOfMove) + Offset
        elif mt==Linear:
            return Distance - CalculatePos_Linear(Distance, FractionOfMove) + Offset
    else :
        Distance = EndPos - StartPos
        Offset = StartPos
        if mt==Accel:
            return CalculatePos_Accel(Distance, FractionOfMove) + Offset
        if mt==AccelDecel:
            return CalculatePos_AccelDecel(Distance, FractionOfMove) + Offset
        if mt==Decel:
            return CalculatePos_Decel(Distance, FractionOfMove) + Offset
        if mt==Linear:
            return CalculatePos_Linear(Distance, FractionOfMove) + Offset
    return 0.0


if __name__ == "__main__":
    print("test")
    wck.connect()
    print("standing up")
    delay_ms(2000)
    print("now")    
    standup(16)
    print("done")   
