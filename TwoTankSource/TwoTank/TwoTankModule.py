'''
Created on Feb 20, 2012

@author: Jeppe
'''
import os
from pymodelica import compile_jmu
from pymodelica import compile_fmu
from pymodelica import compile_fmux
from pyfmi import FMUModel
from pyjmi import JMUModel, CasadiModel

from ModelicaObject import *

import pylab as p
global inited
inited=False;
global TwoTank
def init(modelfile ='../../ModelFiles/TwoTank.mo',model_name = 'TwoSingleTanks'):
    """
    Initialise and set up the instance of the model.
    """
    global inited
    inited=True;
    curr_dir = os.path.dirname(os.path.abspath(__file__));
    
    print curr_dir
    print modelfile

    global TwoTank
    print "starting compilation for "+model_name
    print "... compiling jmu "
    jmuName = compile_jmu(model_name, modelfile)
    jmumodel=JMUModel(jmuName)
    print "... jmu compiled sucessfully"
    print "... compiling fmu"
    fmuName= compile_fmu(model_name,modelfile)
    fmuModel= FMUModel(fmuName)
    print "... fmu compiled sucessfully"
    print "... compiling fmux"
    fmuxModel=None
    """
    fmuxName=compile_fmux(model_name,modelfile)
    fmuxModel=CasadiModel(fmuxName)
    print "... fmux compiled sucessfully"
    """
    TwoTank=ModelicaObject(jmumodel,fmuModel,fmuxModel)
    
def prettyprintTwoTankLinDae():
   
    global inited
    if not inited :
        init()
    global TwoTank
    linJmu=TwoTank.getLinearDaeFromJmu()
    print "##########################Linear DAE MODEL###########################\n" 
    print "E*dx = A*x + B*u + F*w + g"
    for item in linJmu.keys() :
        print " Element : " +item 
        print linJmu.get(item);

def prettyprintTwoTankLinODE():
   
    global inited
    if not inited :
        init()
    global TwoTank
    linJmu=TwoTank.getOdeFromJmu()
    print "##############################ODE MODEL###########################\n" 
    print "dx = A*x + B*u + g "
    print "w = H*x + M*u + q"
    for item in linJmu.keys() :
        print " Element : " +item 
        print linJmu.get(item);
def prettyprintJMUModel():
    print "Found inputs : " 
    
    
    

def plotSim(with_plots=True):
    global inited
    if not inited :
        init()
    global TwoTank
    res = TwoTank.jmu.simulate(final_time=300)
    
    h1 = res['h1']
    h2= res['h2']
    input=res['u1']
    tajjm = res['time']


    if with_plots:
        fig = p.figure(1)
        p.subplot(211)
        p.plot(tajjm,h1,tajjm,h2)
        p.legend(('h1','h2'))
        p.subplot(212)
        p.plot(tajjm, input)
        p.legend(('input'))
        p.grid()
        p.show()
    
if __name__ == '__main__':
    init()
    
    
