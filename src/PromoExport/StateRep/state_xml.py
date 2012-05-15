'''
Created on Mar 26, 2012

@author: Jeppe
'''
from xml.dom.minidom import Document
def getBaseXml(name = "defaultName"):
    doc=Document()
    
    scenario=doc.createElement("Scenario")
    scenario.setAttribute("name", name);
    doc.appendChild(scenario)
  
    childToAdd=doc.createElement("Components")
    scenario.appendChild(childToAdd)
    
    childToAdd=doc.createElement("Variables")
    scenario.appendChild(childToAdd)
    
    
    childToAdd=doc.createElement("Controllers")
    scenario.appendChild(childToAdd)
    
    
    childToAdd=doc.createElement("PortConnectors")
    scenario.appendChild(childToAdd)
    
    childToAdd=doc.createElement("CPortConnectors")
    scenario.appendChild(childToAdd)
    
    childToAdd=doc.createElement("ProcessModels")
    scenario.appendChild(childToAdd)
    
    childToAdd=doc.createElement("Layers")
    scenario.appendChild(childToAdd)
    
    return doc
    

def testPrintXml():
    doca=getBaseXml()
    print doca.toprettyxml(indent="   ")
    