'''
Created on Feb 20, 2012

@author: Jeppe
'''
from pyjmi.linearization import linearize_dae
from pyjmi.linearization import linear_dae_to_ode
from pyjmi import JMUModel
from pymodelica import compile_jmu
from  pyjmi.jmi import JMIException
class ModelicaObject:

    """
    An object, containing instances of the different types of models
    """
    def __init__(self,xmlFile,xmlDoc,rooterrornode):
        
        self.outPutDoc=xmlDoc
        import logging
        logging.basicConfig(level=logging.DEBUG)
        self.errnode=self.outPutDoc.createElement("ModelicaErrors")
        rooterrornode.appendChild(self.errnode)
        
        file_name=xmlFile.getElementsByTagName("filepath")[0].firstChild.nodeValue
        model_name=xmlFile.getElementsByTagName("model")[0].firstChild.nodeValue
        print "starting compilation for the model: "+model_name
        print "In the following file: "+file_name
        # TODO this is just for debugging. uncomment please
        import os
        fileExists=os.path.isfile(file_name)
        if(not fileExists):
            self.putErr("The given Modelica file"+file_name+"does not seem to exist, is the path correct?");
        #jmumodel=JMUModel(jmuName)
        try:
            jmuName = compile_jmu(model_name, file_name)
            #jmumodel=JMUModel(r'.\QuadTankPack_QuadTank.jmu')
            jmumodel=JMUModel(jmuName)
            #print "created the following"+jmuName
            self.jmu=jmumodel;
        except Exception, ex:
            logging.exception("Something awful happened!")
        self.linJmu=None
        
    
    
    def getLinearDaeFromJmu(self):
        """
        Takes a ModelicaObject, and returns a dictionary containing the output
        """
        if(self.linJmu):
            return self.linJmu
        else:
            init_res=self.jmu.initialize()
            (E_dae,A_dae,B_dae,F_dae,g_dae,state_names,input_names,algebraic_names, dx0,x0,u0,w0,t0) = linearize_dae(init_res.model);
            toReturn={"E":E_dae,"A":A_dae,"B":B_dae,"F":F_dae,"g":g_dae,"State_names":state_names,"input_names":input_names,"algebraic_names":algebraic_names,"dx0":dx0,"x0":x0,"u0":u0,"w0":w0,"t0":t0}
            self.linJmu=toReturn;
        return self.linJmu
    
    def putErr(self,toPut, i=1):
        
        errormessnode=self.outPutDoc.createElement("ModelicaError"+str(i))
        errormess=self.outPutDoc.createTextNode(toPut)
    
    
        errormessnode.appendChild(errormess);
        self.errnode.appendChild(errormessnode);
        print self.outPutDoc.toprettyxml();
        i=i+1;
#    def getOdeFromJmu(self):
#        """
#        Takes a ModelicaObject, and returns a dictionary containing the output
#        """
#        
#        dae=self.getLinearDaeFromJmu();
#        (A_ode,B_ode,g_ode,H_ode,M_ode,q_ode) =linear_dae_to_ode(dae["E"],dae["A"],dae["B"],dae["F"],dae["g"])
#        self.odeJmu={"A":A_ode,"B":B_ode,"g":g_ode,"H":H_ode,"M":M_ode,"q":q_ode}
#        
#        return self.odeJmu
##    
#    def getStates(self):
#        return self.getLinearDaeFromJmu()["State_names"]
#    def getInputs(self):
#        return self.getLinearDaeFromJmu()["input_names"]