
import time as tim
import wckmodule as wm
import wckplay as wp
import wckkey as kb


import rbcfaces as rf
 
        
##################################

moves = []
    
def find() :
    servos=[]
    positions=[]
   
    print("searching ...")
    for i in range(0,30) :
        a = wm.getservo(i)
        if (a[1] >=0) :
   
            servos.append(i)  
            positions.append(a[1])   
            
            pd= wm.getPDgain(i)
            g = wm.getIgain(i)  
            d = wm.getIO(i)  
            s = wm.getSpeed(i)
            
            print (f"{i:<2} {a[1]:>3} P={pd[0]} D={pd[1]} I={g[0]} D={d[0]} S={s[0]} A={s[1]}")   
               
    return (servos ,positions)   


def record(x, status=[]) : 
    global moves
    pos=[]
    for s in x :
        a = wm.getservo(s)       
        if a[0]!=0 :
            print("??error - check DCMP mode")
        pos.append(a[1])
        
    if moves==[] :
        pos.append(list(0,0,0,0))
        print ("record: ",pos)   
        moves.append(pos)  
    else :    
        pos.append(status)
        print ("record: ",pos)   
        moves.append(pos)   
    passiv(x)          
    return 

def movea2b(servos,from_pos,to_pos, tq=[], pn=[]) :
    #now complete rest of scene    
    
    #print("movea2b ; ",from_pos,"-->",to_pos)

    status=to_pos[-1] # status? 
    ns =status[1]
    ts =status[0]
        
    # status[0]=total duration, status[1]=no steps, status[2]=mood, status[3]=eyes
    rf.eyes=status[3]
    rf.mood=status[2]
    rf.draw_face()
        
    if (ns==0) or (ts==0) :
        return
    
    if tq == [] :
        tq= [4]*len(servos)
        
    ts = (ts/1000)/ns 
     
    for stp in range(0,ns):  
        #p=[]    
        start=tim.time()  
        for c in range (0, len(servos)) :   
  
            if (stp==0) and (pn !=[]) :
                wm.setIO(servos[c],pn[c])
                     
            wm.setservo(servos[c],tq[c],round(wp.GetMoveValue(wp.Linear, from_pos[c], to_pos[c], float(stp+1)/ns)))
            
            #p.append(round(wp.GetMoveValue(wp.Linear, from_pos[c], to_pos[c], float(stp+1)/ns)))                          
        end=tim.time()  

        q=ts-(end-start)
        #print (f"timer:  {stp}, {(end-start)*1000}ms, {ts*1000}ms  {q*1000}ms")
        if (q>0.005) :
            tim.sleep(q)
        
   
def play(x, move=[], extras=[]) :
    global moves
    
    initpos=[]
    for i in x :
        initpos.append(wm.getservo(i)[1])
            
    if move==[] :
        move=moves
        

    torq=""
    ports=""
    pids=""
        
    if extras != [] :
        torq=extras[0]  # 1 per servo for each scene
        ports=extras[1] # 1 per servo for each scene
                
        #print (f"t={torq}, p={ports}")    
        
        # PIDS
        P=extras[2][0]
        D=extras[2][1]
        I=extras[2][2]
        
        #print (f"p={P}, d={D}, i={I}")  

        for n in range(len(x)) :
            #print(f"Servo {x[n]} = {P[n]}, {D[n]}, {I[n]}")
            wm.setPDgain(x[n],P[n], D[n])
            wm.setIgain(x[n],I[n])      
                
    
    if len(move)== 1 :
        print("single move")
        movea2b(x, initpos, move[0])  
        print("single done") 
        return 
    
    im = move[0]    
    print("(starting point) im=",im)
    status=im[-1]
    ns =status[0]
    
    if ns == 0 :
        print("move to start")
        movea2b(x, initpos, im)
        move = move[1:]
    else :
        print("assume IP is start")   

        
    #now complete rest of scene    
    print("do scene", len(move))
    n=0
    for m in move :  
        #print("scene",n, torq[n], ports[n])   
         
        if torq=="" or ports=="" :
            movea2b(x, im, m)  
        else :
            movea2b(x, im, m, tq=torq[n], pn=ports[n])              
        im=m   
        n+=1   
       
    print ("done.")
    return
      
def passiv(x) :
    for s in x :
        wm.setpassive(s)   
    
def clr() :
    global moves
    print('clr moves')
    moves=[]
    return

def querynset() :
    while True:
        a=input("servo? [q to quit]")
        if a=='q' :
            break
        b = wm.getservo(int(a))
        print("\nservo ",a,"=",b)
        c = input("new pos?")
        if c=='q' :
            break
        print(c,"\n")
        wm.setservo(int(a),4,int(c))
    print("\ndone")
    return	        
        

