within;

  model Sim_QuadTank
    TwoTank qt;
    input Real u1 = qt.u1;
  initial equation
  //der(qt.x1) = 0;
  //der(qt.x2) = 0;
    qt.h1 = 0.0627;
    qt.h2 = 0.06044;
  end Sim_QuadTank;

  model TwoTank
    // Process parameters
	parameter Modelica.SIunits.Area A1=4.9e-4, A2=4.9e-4;
	parameter Modelica.SIunits.Area a1(min=1e-6)=0.03e-4, a2=0.06e-4;
	parameter Modelica.SIunits.Acceleration g=9.82;
	parameter Real pumprate(unit="m^3/s/V") = 2e-6;


    // Initial tank levels
	parameter Modelica.SIunits.Length h1_0 = 0.361265;
	parameter Modelica.SIunits.Length h2_0 = 0.093252;

	
    // Tank levels
	Modelica.SIunits.Length h1(start=h1_0,min=0.0001,max=0.40);
	Modelica.SIunits.Length h2(start=h2_0,min=0.0001,max=0.40);


	// Inputs
	input Real inflow(start=1,min=0,max=4);
  equation
	
    der(h1) = -a1/A1*sqrt(2*g*h1) +inflow;
	der(h2) = -a2/A2*sqrt(2*g*h2) + a1/A1*sqrt(2*g*h1);
					
	

  end TwoTank; 
  
  model TwoSingleTanks
	  SingleTank tank1;
	  SingleTank tank2;
	  input Real pumpflow(start=0.04,min=0,max=0.07);
	  
  equation
	 	tank1.inflow=pumpflow;
		connect(tank1.outflow, tank2.inflow);
  	 
  end TwoSingleTanks;
  
  model SingleTank
    // Process parameters
	parameter Modelica.SIunits.Area A1=4.9e-4;
	parameter Modelica.SIunits.Area a1(min=1e-6)=0.03e-4;
	parameter Modelica.SIunits.Acceleration g=9.82;


    // Initial tank levels
	parameter Modelica.SIunits.Length h1_0 = 0.04;


	
    // Tank levels
	Modelica.SIunits.Length h1(start=h1_0,min=0.0001,max=0.40);



	// Inputs
	input Real inflow;
	
	output Real outflow;

  equation
	outflow=-a1/A1*sqrt(2*g*h1);
    der(h1) =outflow  +inflow;
	
					
	

  end SingleTank;
