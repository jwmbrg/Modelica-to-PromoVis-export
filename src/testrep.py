'''
Created on Mar 7, 2012

@author: Jeppe
'''
import state_rep.pmv_scenario as pmv
import os, sys, inspect
import TwoTank.TwoTankModule as dualtanks
global twoT
global quadT
global d
def run_me():
    print "you have loaded the test module for scenario representations"
    dualtanks.init()
    global d
    d=dualtanks.getTwoTank().getLinearDaeFromJmu()
    global twoT
    twoT=pmv.pmv_scenario(d.get('E'),d.get('A'), d.get('B'),d.get('F'),d.get('g'),d.get('State_names'), d.get('input_names'),d.get('algebraic_names'))

def run_me_quad():
    print "you have loaded the test module for scenario representations"
    dualtanks.initQuad()
    global d
    
    d=dualtanks.getQuadTank().getLinearDaeFromJmu()
    global quadT
    quadT=pmv.pmv_scenario()
        
if __name__ == '__main__':
    
    # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
    # __file__ fails if script is called in different ways on Windows
    # __file__ fails if someone does os.chdir() before
    # sys.argv[0] also fails because it doesn't not always contains the path

    run_me()
    run_me_quad()