'''
Created on Mar 7, 2012

@author: Jeppe
'''

def multTf(a,b):
    return

class pmv_tf(object):
    def __init__(self,num,den,variable):
        '''
        Constructor
        '''
        self.num=num
        self.den=den
        
    def printMe(self):
        i=(len(self.num))-1
        numToPrint=""
        for element in self.num :
            numToPrint += str(element) +'*s^'+str(i)
            i-=1
            
        denToPrint=""
        i=(len(self.den))-1
        for element in self.den :
            if(denToPrint!=""):
                denToPrint+=" + "
            denToPrint += str(element) +'*s^'+str(i)
            i-=1
            
        print numToPrint
        print '---------------------------'
        print denToPrint
            