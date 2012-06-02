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

        
    def __init__(self,matrix_dict,xmlDoc,rooterrornode):
        
        self.outPutDoc=xmlDoc
        
        self.errnode=self.outPutDoc.createElement("ScenarioGenerationErrors")
        rooterrornode.appendChild(self.errnode)
        
        
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
        """for element in self.state_names :
            toReturn.append(self.createStateVar(i))
            i+=1
        i=0
        """
        
        rowSolvDict=self.getRowForNameDict()
        for rowNumber in rowSolvDict.keys():
            theName=rowSolvDict[rowNumber]
            if theName in self.state_names :
                toReturn.append(self.getStateVar(rowNumber, theName))
            else:
                toReturn.append(self.getAlgeBraicVar(rowNumber, theName))
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
    
    def getRowForNameDict(self):
        """ This returns a dictionary with state or algebraic names as keys, and and integer as values.
        The integer represents the row, in the DAE-system, that should be used to solve the state or algebraic variable.
        """
        #Append E|
        state_alg_names=np.append(self.state_names,self.algebraic_names,axis=1);
        E_concat_F=np.append(self.E,self.F,axis=1)

        toRun={}
        rownum=0;
        for element in state_alg_names:
            toRun[element]=[]
      
        for row in E_concat_F:
                colnum=0
                for col in row:
                        if(col!=0):
                                toRun[state_alg_names[colnum]].append(rownum)
                        colnum+=1;
                rownum+=1;
       
        
        algebraic_loop=False;
       
        i=0;
        loops =0
        statesandrows={}
        while toRun and not algebraic_loop:
                element=toRun.keys()[i]
                if(len(toRun[element])==1):
                        loops=0;
                        state=element
                        val=toRun[element][0]
                        
                        statesandrows[val]=state
                        del toRun[element]
                        for remaining in toRun:
                            self.removeRow(toRun[remaining],val )
                        

        
                i+=1
                if(i>=len(toRun)):
                        if(loops==2):
                                algebraic_loop=True
                                self.p
                                print "encountered an algebraic loop"
                        i=0;
                        loops+=1;
        print "found statesandrows"
        return statesandrows;

    def removeRow(self,theList,val):
        if val in theList:
                theList.remove(val)
        return True;
    
    def getAlgeBraicVar(self,rowNumber,var_name):
        Erow=self.E[rowNumber]
        print "EEEROW"
        print Erow
        Arow=self.A[rowNumber]
        Brow=self.B[rowNumber]
        Frow=self.F[rowNumber]
        index=self.algebraic_names.index(var_name)
        
        name=var_name
        typ=type_params.state
        
       

        denominator=np.array([Frow[index]])

            
        print "hoho"
        state_dict={}
        #find all numerators for states, and input the common denominator
        i=0;
        while(i<len(self.state_names)):
            
            derPart=Erow[i]
            numerator=np.array([])
            if(derPart==0):
                numerator=np.array([-Arow[i]])
            else:
                numerator=np.array([derPart,-Arow[i]])

            tf=pmv_tf.pmv_tf(numerator,denominator,self.state_names[i])
            if(Erow[i]!=0 or Arow[i]!=0):
                state_dict[self.state_names[i]]=tf
            i+=1;
        #self.fillDict(coeffarr,state_dict,denominator,index,self.state_names)
        #do the same for inputs
        print "states"
        input_dict={}
        i=0;
        print "working with inputs "+name
        print Brow
        while(i<len(self.input_names)):
            numerator=np.array([-Brow[i]])
            print "numeartor is " +str(numerator) +" and " +str(Brow[i]!=0)
            tf=pmv_tf.pmv_tf(numerator,denominator,self.input_names[i])
            if(Brow[i]!=0):
                print "adding to dict"
                input_dict[self.input_names[i]]=tf
            i+=1;
        
        #self.fillDict(coeffarr, input_dict, denominator, index,self.input_names,True)
        print "mothers"
        
        disturbance_dict={}
        i=0;
        while(i<len(self.algebraic_names)):
            if i!=index:
                numerator=np.array([-Frow[i]])
                tf=pmv_tf.pmv_tf(numerator,denominator,self.algebraic_names[i])
                if(Frow[i]!=0):
                    disturbance_dict[self.algebraic_names[i]]=tf
            i+=1;
            
        
    
        
        toReturn=pmv_variable.pmv_variable(name,typ,state_dict,disturbance_dict,input_dict)
        
        #set working points
        toReturn.workingPoint=str(self.matrix_dict.get("w0")[index])
        return toReturn
    def getStateVar(self,rowNumber,var_name): 
        Erow=self.E[rowNumber]
        print "EEEROW"
        print Erow
        Arow=self.A[rowNumber]
        Brow=self.B[rowNumber]
        Frow=self.F[rowNumber]
        index=self.state_names.index(var_name)
        
        name=var_name
        typ=type_params.state
        
        derPart=Erow[index]
        denominator=np.array([])
        if(derPart==0):
            denominator=np.array([-Arow[index]])
        else:
            denominator=np.array([derPart,-Arow[index]])
            
        print "hoho"
        state_dict={}
        #find all numerators for states, and input the common denominator
        i=0;
        while(i<len(self.state_names)):
            if i!=index:
                derPart=Erow[i]
                numerator=np.array([])
                if(derPart==0):
                    numerator=np.array([Arow[i]])
                else:
                    numerator=np.array([-derPart,Arow[i]])

                tf=pmv_tf.pmv_tf(numerator,denominator,self.state_names[i])
                if(Erow[i]!=0 or Arow[i]!=0):
                    state_dict[self.state_names[i]]=tf
            i+=1;
        #self.fillDict(coeffarr,state_dict,denominator,index,self.state_names)
        #do the same for inputs
        print "states"
        input_dict={}
        i=0;
        print "working with inputs "+name
        print Brow
        while(i<len(self.input_names)):
            numerator=np.array([Brow[i]])
            print "numeartor is " +str(numerator) +" and " +str(Brow[i]!=0)
            tf=pmv_tf.pmv_tf(numerator,denominator,self.input_names[i])
            if(Brow[i]!=0):
                print "adding to dict"
                input_dict[self.input_names[i]]=tf
            i+=1;
        
        #self.fillDict(coeffarr, input_dict, denominator, index,self.input_names,True)
        print "mothers"
        
        disturbance_dict={}
        i=0;
        while(i<len(self.algebraic_names)):
            numerator=np.array([Frow[i]])
            tf=pmv_tf.pmv_tf(numerator,denominator,self.algebraic_names[i])
            if(Frow[i]!=0):
                disturbance_dict[self.algebraic_names[i]]=tf
            i+=1;
            
        
    
        
        toReturn=pmv_variable.pmv_variable(name,typ,state_dict,disturbance_dict,input_dict)
        #set working points
        toReturn.workingPoint=str(self.matrix_dict.get("x0")[index])
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
        print listOfVars
        print self.varArr
        for element in self.varArr:
            for s in listOfVars:
                if element.name==s:
                    element.typ=type_params.measured
                    print "changed type of" +element.name
        return
    def putErr(self,toPut, i=1):
        
        errormessnode=self.outPutDoc.createElement("ModelicaError"+str(i))
        errormess=self.outPutDoc.createTextNode(toPut)
    
    
        errormessnode.appendChild(errormess);
        self.errnode.appendChild(errormessnode);
        print self.outPutDoc.toprettyxml();
        i=i+1;
        