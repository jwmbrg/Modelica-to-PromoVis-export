'''
Created on Mar 26, 2012

@author: Jeppe
'''

class layout_emitter(object):
    '''
    Used to create coordinates for the graphical representation in PromoVis, default is a straight line
    with 30 px spacing
    '''


    def __init__(self,size):
        '''
        Constructor
        '''
        self.startSize=size
        self.currentState=0
        
    def getCord(self):
        """
        Fixme, make sure to throw an exception if currentstate is bigger than startsize
        """
        toReturn=[200+90*self.currentState,400]
        self.currentState+=1;
        return toReturn;
    def reset(self):
        self.currentState=0;