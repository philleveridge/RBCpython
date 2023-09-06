db={}
DBNAME="db.txt"

def store(name="") :
    global db

    if (name=="") :
        name=DBNAME
        
    try :
        f= open(name,"w")
        f.write(str(db))
        f.close()
        print("Database saved")
    except :
        print ("Error cant save db")
        
def load(name=""):
    global db
    
    if (name=="") :
        name=DBNAME
    else :
        DBNAME=name

    try :
        f=open(name,"r")
        b=f.read()
        db=eval(b)
        print("DB load")
    except FileNotFoundError:
        print ("No db file")   
        
def insert(t,d):
    global db
    db[t] = d
    
def get(t):
    global db
    if t in db :
        return db[t]
    else :
        return ""

def exists(n):
    if n in db :
        return True
    else :
        return False
              
def show() :
    global db
    print ("DB contains ", len(db), " entries")
    for k in db :
        print(f"{k:<10} : {len(db[k])} : {str(db[k])[0:30]}")
      
def clear(name=""):
    global db
    print("DB clear")
    db={}
    if (name != "") :
        DBNAME=name


if __name__ == '__main__':
# Use like this

    clear()
    
    insert("red", [[2,3,4],[4,5,6]])
    insert("blue", [[1,2,3],[4,5,6]])

    show()
    
    store()
    
    clear()
    
    show()
    
    load()
    
    show()
    
    insert("green", [[1,2,3],[4,5,6]])    
    
    show()
    
    print ("red=", get("red"))
    
    
    
    

