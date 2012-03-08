'''
Created on Mar 7, 2012

@author: Jesper Moberg
'''

class pmv_variable(object):
    '''
    classdocs
    '''


    def __init__(self,name,type,matrix_dict={},disturbance_dict={},input_dict={}):
        '''
        Constructor
        '''
        self.name=name
        self.state_dict=matrix_dict
        self.disturbance_dict=disturbance_dict
        self.input_dict=input_dict
        self.type=type
    
    def printMe(self):
        print "|||||||||||||||||||||||||||||||||||"
        print ""
        print "Variable " +self.name
        print ""
        print "|||||||||||||||||||||||||||||||||||"
        print ""
        if(len(self.state_dict)!=0):
            print "#################################"
            print ""
            print "Dependencies of other states for  " +self.name
            print ""
            print "#################################"
            print ""
            for name, value in self.state_dict.iteritems(): 
                print "The Transfer function from " +name +" to " +self.name +" is: "
                print ""
                value.printMe()
                print ""
            print ""
        
        if(len(self.input_dict)!=0):
            print "#################################"
            print ""
            print "Dependencies of declared inputs " +self.name
            print ""
            print "#################################"
            print ""
            for name, value in self.input_dict.iteritems(): 
                print "The Transfer function from " +name +" to " +self.name +" is: "
                print ""
                value.printMe()
                print ""
            print ""
            
        print ""
        print ""
        print ""