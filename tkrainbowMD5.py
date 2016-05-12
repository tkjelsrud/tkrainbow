# Python - Find my hash
#
# LK 2ab96390c7dbe3439de74d0c9b0b1767
#
import sys
import hashlib
import datetime
from multiprocessing import Pool
   

class Cog:
    Iter = 0
    Min = 48-1 #0 = crap chars, #32 = Space, #48 = 0
    Max = 127 #256  #sys.maxunicode
    
    def __init__(self, chNum = 0, fT = None, fH = None):
        self.i = Cog.Min
        self.cnt = 0
        self.child = None
        self.findT = fT
        self.findH = fH
        self.startTime = datetime.datetime.now()
        self.parent = None
        
        for i in range(1, chNum):
            self.addCog()
    
    def get(self):
        u = ""
        try:
            u = chr(self.i)#unichr
        except:
            None
            
        if self.child:
            u = u + self.child.get()
        
        return u
    
    def childOrNext(self):
        Cog.Iter = Cog.Iter + 1
        self.cnt = self.cnt + 1
        
        if self.child and not self.child.isEnd():
            self.child.childOrNext()
        else:
            self.i = self.i + 1
            
            if not self.parent:
                # We are the top
                print("(Primary cog iteration)")
            
            if self.child:
                self.child.resetAll()
            
    def isEnd(self):
        return self.i == Cog.Max
    
    def reset(self):
        self.i = Cog.Min
    
    def resetAll(self):
        self.i = Cog.Min
        if self.child:
            self.child.resetAll()

    def addCog(self):
        if self.child:
            self.child.addCog()
        else:
            self.child = Cog()
            self.child.parent = self

    def numCog(self):
        if self.child:
            return 1 + self.child.numCog()
        else:
            return 1
    
    def cntAll(self):
        if self.child:
            return self.cnt + self.child.cntAll()
        else:
            return self.cnt

    def spool(self, x):
        self.i = self.i + x
            
    def itrLeft(self):
        x = (Cog.Max + 1) - self.i
        if self.child:
            return x * self.child.itrLeft()
        else:
            return x

            # len: 7, 3 cpu, pr cpu: 562 949 953 421 312
            # Total: 1688849860263936
            # 32^7 : 34359738368
            
def Report(c, pid = ""):
    elapsed = datetime.datetime.now() - c.startTime
    elapSec = elapsed.total_seconds()
    if elapSec == 0:
        elapSec = 0.01
    print(pid + " cogs: " + str(c.numCog()) + ", cnt: " + str(c.cntAll()) + ", time used: " + str(elapsed) + ", itr/sec: " + str(c.cntAll()/float(elapSec)) + " itr/left: " + str(c.itrLeft()))

def ProcessRange(c, n, m):
    #Report(c, "[STA] P" + str(n) + "#" + str(m) + " fT:" + str(c.findT) + " fH:" + str(c.findH))
    
    
    for i in range(n, m): 
        c.spool(i) # Set from value
        Report(c, "[ST] P" + str(i) + "#" + str(m))
        while not c.isEnd() and not c.i == m:
            s = c.get()
            
            x = hashlib.md5(s.encode('utf-8')).hexdigest()
            
            if c.findH and x == c.findH:
                print("FOUND --> " + s + " --> " + x)
                return True
                
            if c.findT and s == c.findT:
                print("FOUND --> " + s + " --> " + x)
                return True
                
            c.childOrNext()
        c.resetAll()
        
    Report(c, "[END] P" + str(n) + "#" + str(m))
                
def RunRange(inp):
    c = inp[0]
    idx = inp[1]
    n = ((Cog.Max - Cog.Min) / CPU) * idx
    m = n + ((Cog.Max - Cog.Min) / CPU)
    try:
        ProcessRange(c, int(n), int(m))
        Report(c, "[END] P")
    except KeyboardInterrupt:
        Report(c)
        print("User cancel")
        pass

CPU = 4           

if __name__ == '__main__':
    findText = None
    nCog = 0
    
    if len(sys.argv) > 1:
        findText = sys.argv[1]
        
        if len(sys.argv) > 2:
            nCog = int(sys.argv[2])
    tries = 0
    outHash = False
    stopFind = False
    guess = ""
    accguess = ""
    find = None
    
    print("FIND: " + findText)
    
    c = Cog(nCog)
    
    c.findT = findText
    c.findH = None
    if len(findText) == 32:
        c.findH = findText
        c.findT = None

    
    p = Pool(CPU)
    prArr = []
    for i in range(0, CPU):
        prArr.append((c, i))
    
    p.map(RunRange, prArr)