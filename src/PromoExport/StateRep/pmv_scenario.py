'''
Created on Mar 7, 2012

@author: Jesper Moberg
'''
import pmv_tf
import pmv_variable
import numpy as np
import layout_emitter
from xml.dom.minidom import Document
class default_values(object):
        posInf="Inf"
        negInf="-Inf"
        specEmptyVal=""
        specVal="0.0"
    
class type_params(object):
    input=0
    state=1
    disturbance=2
    measured=3

class pmv_scenario(object):
    '''
    classdocs
    '''

        
    def __init__(self,matrix_dict):
        '''
        Constructor
        Assumes E to be identity
        '''
        self.name="fixme"
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
        i=0
        for element in self.input_names :
            toReturn.append(self.createInputVar(i))
            i+=1
            
      
        return toReturn
    
    def createInputVar(self,index):
        name=self.input_names[index]
        typ=type_params.input
        toReturn=pmv_variable.pmv_variable(name,typ)
        toReturn.workingPoint=str(self.matrix_dict.get("u0")[index])
        return toReturn
    
    
    def createStateVar(self,index):
        name=self.state_names[index]
        # print name
        typ=type_params.state
        
        
        dividerCoeff=self.E[index][index]
 
        coeffarr=self.A[index]
        #create the common denominator
        i=0
       
      
        for element in coeffarr:
            if(i==index):
                denominator=np.array([dividerCoeff, -element])
               # denominator=denominator*dividerCoeff
            i+=1


        
        state_dict={}
        #find all numerators for states, and input the common denominator
        self.fillDict(coeffarr,state_dict,denominator,index,self.state_names)
        #do the same for inputs
        input_dict={}
        
        coeffarr=self.B[index]
        self.fillDict(coeffarr, input_dict, denominator, index,self.input_names,True)
        
        
        disturbance_dict=0
        
        
    
        
        toReturn=pmv_variable.pmv_variable(name,typ,state_dict,disturbance_dict,input_dict)
        toReturn.workingPoint=str(self.matrix_dict.get("x0")[index])
        
        return toReturn
    
    
    def fillDict(self, coeffarr,toDict,denominator,index,picknames,notState=False):
        state=0
       # print "coeffarr is :"
        #print coeffarr
        #find transfer function
        for  element in coeffarr:
            #print element
            if(element!=0 and (state!=index or notState)):
                numerator=[element]
                varName=picknames[state]
                tf=pmv_tf.pmv_tf(numerator,denominator,varName)
                toDict[varName]=tf
                #print toDict
            state+=1
        #print "created"
        #print toDict
    
    def sanityCheck(self):
        '''
        Unimplemented, here we should examine the set points, so that the derivatives
        are "sufficiently" close to zero"
        '''
    
    def printMe(self):
        for element in self.varArr:
            element.printMe()
            
    def getNumOfType(self,type):
        toCount=[x for x in self.varArr if x.typ==type]
        return len(toCount)
        
    def getAsXML(self):
        doc=Document()
    
        scenario=doc.createElement("Scenario")
        scenario.setAttribute("name", self.name);
        doc.appendChild(scenario)
  
        childToAdd=doc.createElement("Components")
        scenario.appendChild(childToAdd)
    
        childToAdd=doc.createElement("Variables")
        le=layout_emitter.layout_emitter(self.getNumOfType(type_params.input),self.getNumOfType(type_params.state),self.getNumOfType(type_params.measured))
        for element in self.varArr :
            childToAdd.appendChild(element.getAsXMLVariable(doc,le))
        
        
        scenario.appendChild(childToAdd)
    
    
        childToAdd=doc.createElement("Controllers")
        scenario.appendChild(childToAdd)
    
    
        childToAdd=doc.createElement("PortConnectors")
        scenario.appendChild(childToAdd)
    
        childToAdd=doc.createElement("CPortConnectors")
        scenario.appendChild(childToAdd)
    
        childToAdd=doc.createElement("ProcessModels")
        for element in self.varArr :
            toAdd=element.getAsXMLProcessModel(doc)
            if(toAdd==None):
                pass
            else:
                childToAdd.appendChild(toAdd)
        scenario.appendChild(childToAdd)
    
        childToAdd=doc.createElement("Layers")
        scenario.appendChild(childToAdd)
        #print doc.toprettyxml(indent="   ")
       
        #fileObj = open("test.pmv","w") 
        #fileObj.write(doc.toprettyxml())
        #fileObj.close()
        return doc
    
    def setMeasuredVars(self,listOfVars):
        for element in self.varArr:
            for s in listOfVars:
                if element.name==s:
                    element.typ=type_params.measured
                    print "changed type of" +element.name
        return
        