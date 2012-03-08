'''
Created on Feb 20, 2012

@author: Jeppe
'''
from pyjmi.linearization import linearize_dae
from pyjmi.linearization import linear_dae_to_ode
class ModelicaObject:
    """
    An object, containing instances of the different types of models
    """
    def __init__(self,jmu):
        self.jmu=jmu;

        self.linJmu=None;
    
    def getLinearDaeFromJmu(self):
        """
        Takes a ModelicaObject, and returns a dictionary containing the output
        """
        
        init_res=self.jmu.initialize()
        (E_dae,A_dae,B_dae,F_dae,g_dae,state_names,input_names,algebraic_names, dx0,x0,u0,w0,t0) = linearize_dae(init_res.model);
        self.linJmu={"E":E_dae,"A":A_dae,"B":B_dae,"F":F_dae,"g":g_dae,"State_names":state_names,"input_names":input_names,"algebraic_names":algebraic_names,"dx0":dx0,"x0":x0,"u0":u0,"w0":w0,"t0":t0}
        
        return self.linJmu
    def getOdeFromJmu(self):
        """
        Takes a ModelicaObject, and returns a dictionary containing the output
        """
        
        dae=self.getLinearDaeFromJmu();
        (A_ode,B_ode,g_ode,H_ode,M_ode,q_ode) =linear_dae_to_ode(dae["E"],dae["A"],dae["B"],dae["F"],dae["g"])
        self.odeJmu={"A":A_ode,"B":B_ode,"g":g_ode,"H":H_ode,"M":M_ode,"q":q_ode}
        
        return self.odeJmu
    
    def getStates(self):
        return self.getLinearDaeFromJmu()["State_names"]
    def getInputs(self):
        return self.getLinearDaeFromJmu()["input_names"]