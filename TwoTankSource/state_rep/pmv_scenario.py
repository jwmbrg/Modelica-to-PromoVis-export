'''
Created on Mar 7, 2012

@author: Jesper Moberg
'''
import pmv_tf
import pmv_variable
import numpy as np
class pmv_scenario(object):
    '''
    classdocs
    '''
    
    class _type_params(object):
        _input=0
        _state=1
        _disturbance=2
        
    def __init__(self,matrix_dict):
        '''
        Constructor
        Assumes E to be identity
        '''
        
        self.E=matrix_dict.get('E')
        self.A=matrix_dict.get('A')
        self.B=matrix_dict.get('B')
        self.F=matrix_dict.get('F')
        self.g=matrix_dict.get('g')
        self.state_names=matrix_dict.get('State_names')
        self.input_names=matrix_dict.get('input_names')
        self.algebraic_names=matrix_dict.get('algebraic_names')
        self.matrix_dict=matrix_dict
        self.varArr=self.createModel();
        self.sanityCheck()
        
        
    def createModel(self):
        global toReturn
        toReturn=[]
        i=0
        for element in self.state_names :
            toReturn.append(self.createStateVar(i))
            i+=1
        return toReturn
    
    
    def createStateVar(self,index):
        name=self.state_names[index]
        print name
        typ=self._type_params._state
        
        
        dividerCoeff=self.E[index][index]
 
        coeffarr=self.A[index]
        #create the common denominator
        i=0
       
      
        for element in coeffarr:
            if(i==index):
                denominator=np.array([1.0, -element])
                denominator=denominator*dividerCoeff
            i+=1


        
        state_dict={}
        #find all numerators for states, and input the common denominator
        self.fillDict(coeffarr,state_dict,denominator,index,self.state_names)
        #do the same for inputs
        input_dict={}
        
        coeffarr=self.B[index]
        self.fillDict(coeffarr, input_dict, denominator, index,self.input_names,True)
        
        
        disturbance_dict=0
        toReturn= pmv_variable.pmv_variable(name,typ,state_dict,disturbance_dict,input_dict)
        
        return toReturn
    
    
    def fillDict(self, coeffarr,toDict,denominator,index,picknames,notState=False):
        state=0
        print "coeffarr is :"
        print coeffarr
        #find transfer function
        for  element in coeffarr:
            print element
            if(element!=0 and (state!=index or notState)):
                numerator=[element]
                varName=picknames[state]
                tf=pmv_tf.pmv_tf(numerator,denominator,varName)
                toDict[varName]=tf
                print toDict
            state+=1
        print "created"
        print toDict
    
    def sanityCheck(self):
        '''
        Unimplemented, here we should examine the set points, so that the derivatives
        are "sufficiently" close to zero"
        '''
    
    def printMe(self):
        for element in self.varArr:
            element.printMe()
            