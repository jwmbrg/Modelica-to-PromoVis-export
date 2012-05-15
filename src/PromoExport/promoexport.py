'''
Created on May 15, 2012

@author: Jeppe
'''
from xml.dom.minidom import parse
from ModelicaObject import ModelicaObject as ModelicaObject
from xml.dom.minidom import Document
from StateRep.pmv_scenario import pmv_scenario
import string
import numpy
launchParams=None
moObject=None
outPutDoc=None
errnode=None
rooterrnode=None
scenarioObj=None
def startExport():
    global launchParams, moObject,scenarioObj
    
    
    if(launchParams):
        print "Starting export"
        moObject=ModelicaObject(launchParams,outPutDoc,rooterrnode)
    else:
        putErr("Unknown error, no parameters seems to be given")
    #print outPutDoc.toprettyxml();
    #jmodelica options should be performed here
    
    #generate the internal represenatation
    matrix_dict=moObject.getLinearDaeFromJmu();
    scenarioObj=pmv_scenario(matrix_dict)
    #print scenarioObj.getAsXML()
    varArr=matrix_dict.get("State_names")+matrix_dict.get("input_names");
    toSetAsMeasured=[x for x in varArr if isMeasured(x)]
    if(toSetAsMeasured):
        print "Given measured variables are: "+str(toSetAsMeasured);
    else:
        print "No variables is declared as measured"
    
def isMeasured(varName):
    
    extensions=launchParams.getElementsByTagName("mpattern")
    if extensions[0].firstChild :
        listOfPatterns=string.split(extensions[0].firstChild.nodeValue, ";")
    else:
        listOfPatterns=[u"_pmvvar"]
    
    
   
    import re
    for element in listOfPatterns:
        pattern=".*"+element
        regExp=re.compile(pattern)
        if(regExp.search(varName)):
            #print "found"
            #print(regExp.findall(varName))
            return True; 
   
    return False;
def runXML(pathString):
    global launchParams
    launchParams=parse(pathString)
    startExport()

    

def run(xmlOrAbsString):
    print "reading "+xmlOrAbsString
    import os.path
    global outPutDoc, errnode, rooterrnode
    
    outPutDoc=Document();
    rootnode=outPutDoc.createElement("root")
    outPutDoc.appendChild(rootnode)
    
    rooterrnode=outPutDoc.createElement("Errors")
    rootnode.appendChild(rooterrnode)
    
    errnode=outPutDoc.createElement("FileErrors")
    rooterrnode.appendChild(errnode)
    
    fileExists=os.path.isfile(xmlOrAbsString)
    if(fileExists and isXml(xmlOrAbsString)):
        print "Loading XML"
        runXML(xmlOrAbsString);
        
        
    elif(fileExists and isAbsPath(xmlOrAbsString)):
        
        print "(Not Implemented)Loading pmv file"
    else :
        putErr("Loading of file failed, have you supplied the correct path")



def isXml(pathString):
    import re
    print "Looking for XML... ",
    regExp=re.compile(r"^[\-a-zA-Z\:\\\.]*\.[xX][mM][lL]")
    if(regExp.search(pathString)):
        #print(regExp.findall(pathString))
        print "Found!"
        return True
    else :
        "Not Found."
        return False;
   
def isAbsPath(pathString):
    import re
    print "Looking for pmv... ",
    regExp=re.compile(r"^[\-a-zA-Z\:\\\.]*\.[xX][mM][lL]")
    if(regExp.search(pathString)):
        print "Found!"
        return True
    else :
        print "Not Found."
        return False;

def putErr(toPut, i=1):
    global errnode,outPutDoc
    errormessnode=outPutDoc.createElement("FileError"+str(i))
    errormess=outPutDoc.createTextNode(toPut)
    
    
    errormessnode.appendChild(errormess);
    errnode.appendChild(errormessnode);
    print outPutDoc.toprettyxml();
    i=i+1;
if __name__ == '__main__':
    import sys
    
    run(sys.argv[1])
    
    
#def doFileExist(pathString):
#    toReturn=False;
#    try:
#        open(pathString, 'w')
#        toReturn=True
#    except OSError:
#        print "File didnt exist, aborting."# handle error here
#    return toReturn