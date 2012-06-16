'''
Created on Mar 7, 2012

@author: Jesper Moberg
'''

import pmv_scenario as pmv
from xml.dom.minidom import Document
import layout_emitter as le
class pmv_variable(object):
    '''
    classdocs
    '''


    def __init__(self,name,typ,matrix_dict={},disturbance_dict={},input_dict={}):
        '''
        Constructor
        '''
        self.name=name
        self.state_dict=dict(matrix_dict.items()+disturbance_dict.items())
        self.disturbance_dict=disturbance_dict
        self.input_dict=input_dict
        self.typ=typ
        
        self.saturationMax=pmv.default_values.posInf
        self.saturationMin=pmv.default_values.negInf
        self.rangeSatMax=pmv.default_values.posInf
        self.rangeSatMin=pmv.default_values.negInf;
        self.workingPoint=pmv.default_values.specEmptyVal
        self.variance=pmv.default_values.specEmptyVal
        self.delay=pmv.default_values.specVal
        self.sample_time=pmv.default_values.specVal
        self.rateLimiter=pmv.default_values.posInf
        self.variance=pmv.default_values.specEmptyVal
        self.delay=str(0.0)
        self.resolution=pmv.default_values.specEmptyVal
    
    def printMe(self):
        print "|||||||||||||||||||||||||||||||||||"
        print ""
        print "Variable " +self.name 
        print "Working point:"
        print self.workingPoint
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
        
    """
    Methods for creating the ProcessModel node in xml
    """
    def getAsXMLProcessModel(self,doc):
        if((len(self.input_dict)+len(self.state_dict))==0):
            return None;
        if(self.typ==pmv.type_params.input):
            return None
        toReturn=doc.createElement("ProcessModel")
        toReturn.appendChild(doc.createElement("ScaledObject"))
        
        
        inputNode=doc.createElement("Inputs")
        toAdd=None
        for element in self.input_dict:
            toAdd=doc.createElement("InVar")
            toAdd.setAttribute("name",element);
            inputNode.appendChild(toAdd)
        for element in self.state_dict:
            toAdd=doc.createElement("InVar")
            toAdd.setAttribute("name",element);
            inputNode.appendChild(toAdd)
        toReturn.appendChild(inputNode)
        
        outputNode=doc.createElement("Outputs")
        toAdd=doc.createElement("OutVar")
        toAdd.setAttribute("name",self.name)
        outputNode.appendChild(toAdd)
        toReturn.appendChild(outputNode)
        
        toAdd=doc.createElement("SampleTime")
        toAdd.appendChild(self.mkValueNode("SpecifiedValue", self.sample_time, doc))
        toReturn.appendChild(outputNode)
        
        pmd=doc.createElement("PMD")
        tfData=doc.createElement("TransferFunctionData")
        tfData.appendChild(self.getModelDataNode(doc))
        tfData.appendChild(self.getNumeratorNode(doc))
        tfData.appendChild(self.getDenominatorNode(doc))
        tfData.appendChild(self.getUncertainityNode(doc))
        tfData.appendChild(self.getChannelDelayNode(doc))
        pmd.appendChild(tfData)
        toReturn.appendChild(pmd)
        return toReturn
        
    def getModelDataNode(self,doc):
        toReturn=doc.createElement("ModelData")
        toReturn.setAttribute("inputs",str(len(self.input_dict)+len(self.state_dict)))
        toReturn.setAttribute("outputs","1")
        return toReturn
    
    def getNumeratorNode(self,doc):
        toReturn=doc.createElement("Numerator")
        toAdd=doc.createElement("CellArray")
        toAdd.setAttribute("T","promovis.misc.SpecifiedDoubleArray")
        toAdd.setAttribute("rows","1")
        toAdd.setAttribute("columns",str(len(self.input_dict)+len(self.state_dict)))
        first=True
        toSet="{"
        for element in self.input_dict :
            if(not first):
                toSet+=","
            first=False
            toSet+=str(self.input_dict.get(element).num.tolist())
            print toSet
        
        for element in self.state_dict :
            if(not first):
                toSet+=","
            first=False
            toSet+=str(self.state_dict.get(element).num.tolist()) 
            print toSet
        toSet+="}"
        toAdd.setAttribute("v",toSet)
        toReturn.appendChild(toAdd)        
        return toReturn
    def getDenominatorNode(self,doc):
        toReturn=doc.createElement("Denominator")
        toAdd=doc.createElement("CellArray")
        toAdd.setAttribute("T","promovis.misc.SpecifiedDoubleArray")
        toAdd.setAttribute("rows","1")
        toAdd.setAttribute("columns",str(len(self.input_dict)+len(self.state_dict)))
        first=True
        toSet="{"
        for element in self.input_dict :
            if(not first):
                toSet+=","
                first=False
            toSet+=str(self.input_dict.get(element).den.tolist())
        for element in self.state_dict :
            if(not first):
                toSet+=","
                first=False
            toSet+=str(self.state_dict.get(element).den.tolist()) 
        toSet+="}"
        toAdd.setAttribute("v",toSet)
        toReturn.appendChild(toAdd)
        return toReturn
    
    def getUncertainityNode(self,doc):
        return self.mkValueNode("Uncertainty", "0", doc)
    
    def getChannelDelayNode(self,doc):
        toReturn=doc.createElement("ChannelDelay")
        toAdd=doc.createElement("CellArray")
        toAdd.setAttribute("T","promovis.misc.NonNegativeValue")
        toAdd.setAttribute("rows","1")
        toAdd.setAttribute("columns",str(len(self.input_dict)+len(self.state_dict)))
        
        first=True
        toSet="{"
        for element in self.input_dict :
            if(not first):
                toSet+=","
                
            toSet+="0.0"
            first=False
        for element in self.state_dict :
            if(not first):
                toSet+=","
                
            toSet+="0.0"
            first=False
        toSet+="}"
        toAdd.setAttribute("v",toSet)
        toReturn.appendChild(toAdd)
        
        return toReturn
    
    """
    Methods for creating the variable node in XML
    """
    def getAsXMLVariable(self,doc,layoutFactory):
        toReturn=None
        
        if(self.typ==pmv.type_params.input):
            toReturn=doc.createElement("ControlVariable")
        elif(self.typ==pmv.type_params.measured):
            toReturn=doc.createElement("MeasuredVariable")
        else:
            toReturn=doc.createElement("InternalVariable")
            
            
            
        contentNode=doc.createElement("Variable")
        contentNode.setAttribute("comp", "          ");
        contentNode.setAttribute("tag", "")
        contentNode.appendChild(self.getNSONode(doc,layoutFactory))
        contentNode.appendChild(self.getSaturationNode(self.saturationMax,self.saturationMin,doc))
        contentNode.appendChild(self.getRangeNode(doc))
        contentNode.appendChild(self.getWPNode(doc))
       
        if(self.typ==pmv.type_params.input):
            contentNode.appendChild(self.getRLNode(doc))
        elif(self.typ==pmv.type_params.state):
            pass
        contentNode.appendChild(self.getVarNode(doc))
        contentNode.appendChild(self.getDelayNode(doc))
        contentNode.appendChild(self.getResNode(doc))
        toReturn.appendChild(contentNode)
        

        
        return toReturn
    
    def getNSONode(self, doc,layoutFactory):
        toReturn=doc.createElement("NamedScenarioObject")
        
        scenObj=doc.createElement("ScenarioObject")
        toAdd=doc.createElement("ScaledObject")
        scenObj.appendChild(toAdd)
        scenObj.appendChild(self.getPrefSizeNode(doc))
        scenObj.appendChild(self.getPosNode(doc,layoutFactory))
        toReturn.appendChild(scenObj)
        toAdd=doc.createElement("Name")
        toAdd.setAttribute("v",self.name)
        toAdd.setAttribute("visible","true")
        toAdd.appendChild(self.getPosOffset(doc))
        toReturn.appendChild(toAdd)
        toReturn.appendChild(self.getDescriptionNode(doc))
        
        return toReturn
    
    def getPosNode(self, doc,layoutFactory):
        if(self.typ==pmv.type_params.measured):
            gurka=layoutFactory.getMeasCord()
        elif self.typ==pmv.type_params.state:
            gurka=layoutFactory.getInternalCord()
        elif self.typ==pmv.type_params.input :
            gurka=layoutFactory.getControlCord()
            print "emitting ann input" +self.name
        else:
            gurka=layoutFactory.getInternalCord()
        toReturn=doc.createElement("Position")
        toReturn.setAttribute("x",str(gurka[0]))
        toReturn.setAttribute("y",str(gurka[1]))
        return toReturn
    
    
    def getPrefSizeNode(self,doc):
        toReturn=doc.createElement("PreferredSize")
        toReturn.setAttribute("width","40")
        toReturn.setAttribute("height","40")
        return toReturn
    def getPosOffset(self,doc):
        toReturn=doc.createElement("PositionOffset")
        toReturn.setAttribute("x","15")
        toReturn.setAttribute("y","15")
        return toReturn
    def getDescriptionNode(self,doc):
        return self.mkValueNode("Description", "", doc)
    
    def getSaturationNode(self,maxS,minS,doc=Document()):
        toReturn=doc.createElement("Saturation")
        
        minSat=doc.createElement("Min")
        
        specMin=self.mkValueNode("SpecifiedValue", minS, doc)
        minSat.appendChild(specMin)
        
        maxSat=doc.createElement("Max")
        specMax=self.mkValueNode("SpecifiedValue",maxS, doc)
        maxSat.appendChild(specMax)
        
        toReturn.appendChild(minSat)
        toReturn.appendChild(maxSat)
        
        return toReturn
    
    def getRangeNode(self,doc=Document()):
        toReturn=doc.createElement("Range")
        toReturn.appendChild(self.getSaturationNode(self.rangeSatMax, self.rangeSatMin,doc))
        return toReturn
    
    def getWPNode(self,doc=Document()):
        toReturn=doc.createElement("WorkingPoint")
        if(self.workingPoint==pmv.default_values.specEmptyVal):
            toReturn.appendChild(self.mkValueNode("SpecifiedEmptyValue",pmv.default_values.specEmptyVal))
        else:
            toReturn.appendChild(self.mkValueNode("SpecifiedEmptyValue",self.workingPoint))
        return toReturn
    
    def getRLNode(self,doc=Document()):
        toReturn=doc.createElement("WorkingPoint")
        toReturn.appendChild(self.mkValueNode("SpecifiedValue", self.rateLimiter,doc))
        return toReturn
    def getVarNode(self,doc=Document()):
        toReturn=doc.createElement("Variance")
        if(self.variance==pmv.default_values.specEmptyVal):
            toReturn.appendChild(self.mkValueNode("SpecifiedEmptyValue",self.variance,doc))
        else:
            toReturn.appendChild(self.mkValueNode("SpecifiedValue",self.variance,doc))
        return toReturn
    def getDelayNode(self,doc=Document()):
        toReturn=doc.createElement("Delay")
        toReturn.appendChild(self.mkValueNode("SpecifiedValue", self.delay,doc))
        return toReturn
    def getResNode(self,doc=Document()):
        return self.mkValueNode("Resolution", self.resolution, doc)
    def mkValueNode(self,name,value, doc=Document()):
        toReturn=doc.createElement(name)
        toReturn.setAttribute("v",value)
        return toReturn
        
        