'''
Created on Mar 7, 2012

@author: Jeppe
'''
#import state_rep.pmv_scenario as pmv
from pyjmi.linearization import linearize_dae
from pyjmi.linearization import linear_dae_to_ode
from pyjmi import JMUModel
from pymodelica import compile_jmu
from  pyjmi.jmi import JMIException
import os, sys, inspect
import TwoTank.TwoTankModule as dualtanks
global twoT
global quadT
global d
global jmu
def run_me_quad():
    global jmu
    print "you have loaded the test module for scenario representations"
    try:
       #jmuName = compile_jmu(model_name, file_name)
       #jmumodel=JMUModel(r'.\QuadTankPack_QuadTank.jmu')
       jmumodel=JMUModel("./TwoTank.jmu")
       #print "created the following"+jmuName
       jmu=jmumodel;
    except Exception, ex:
        print "oops"
        
if __name__ == '__main__':
    
    # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
    # __file__ fails if script is called in different ways on Windows
    # __file__ fails if someone does os.chdir() before
    # sys.argv[0] also fails because it doesn't not always contains the path

   
    run_me_quad()