'''
Created on Mar 26, 2012

@author: Jeppe
'''
import math
import math
class layout_emitter(object):
    '''
    Used to create coordinates for the graphical representation in PromoVis, default is a straight line
    with 30 px spacing
    '''
    SPACINGCONSTANT = 90

    def __init__(self,controls,internals,measureds):
        '''
        Constructor
        '''
        print "initialized an emitter with control :"+str(controls)+"internal: "+str(internals) +"and measureds: "+str(measureds)
        self.currentState=0;
        self.noControls=controls
        self.noInternals=internals
        self.noMeasureds=measureds;
        largest=max(self.noControls,self.noInternals,self.noMeasureds)
        
        self.r=0
        
        self.afMeas=0;
        
        self.measCurr=0;
        self.internalCurr=0;
        self.controlCurr=0;
        self.afControls=0;
        if(largest==self.noControls):
            self.r=((self.noControls-1)*self.SPACINGCONSTANT)/2
        elif(largest==self.noMeasureds):
            self.r=((self.noMeasureds-1)*self.SPACINGCONSTANT)/2
        else:
            self.r=((self.noInternals-1)*self.SPACINGCONSTANT)/2
        self.initCounters()
        

    def initCounters(self):
        if(self.noMeasureds!=0):
            self.afMeas=3.14/(self.noMeasureds-1)
        else:
            self.afMeas=0;
            
        if(self.noControls!=0):
            self.afControls=3.14/(self.noControls-1)
        else:
            self.afControls=0;
        return
    
    def getMeasCord(self):
        toReturnX=self.r+20+self.r+self.r*math.cos(3.14+self.afMeas*self.measCurr)
        toReturnY=self.r+20+self.r*math.sin(3.14+self.afMeas*self.measCurr)
        self.measCurr+=1
        return [int(toReturnX),int(toReturnY)]
    
    def getInternalCord(self):
        toReturnX=self.r+20+self.internalCurr*self.SPACINGCONSTANT
        toReturnY=self.r+20+self.SPACINGCONSTANT
        self.internalCurr+=1
        return [int(toReturnX),int(toReturnY)]
    def getControlCord(self):
        toReturnX=self.r+20+self.r+self.r*math.cos(3.14+self.afControls*self.controlCurr)
        toReturnY=self.r+20+2*self.SPACINGCONSTANT+self.r*math.sin(3.14-self.afControls*self.controlCurr)
        self.controlCurr+=1
        return [int(toReturnX),int(toReturnY)]    
        
            
                                     
    

    def getCord(self):
        """
        Fixme, make sure to throw an exception if currentstate is bigger than startsize
        """
        toReturn=[200+90*self.currentState,400]
        self.currentState+=1;
        return toReturn;
    def reset(self):
        self.currentState=0;