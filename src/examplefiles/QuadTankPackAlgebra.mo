package QuadTankPack

  model Sim_QuadTank
    QuadTank qt;
    input Real u1 = qt.u1;
    input Real u2 = qt.u2;
  initial equation
  //der(qt.x1_pmv) = 0;
  //der(qt.x2) = 0;
    qt.x1_pmv = 0.0627;
    qt.x2 = 0.06044;
    qt.x3 = 0.024;
    qt.x4_blabla = 0.023;
  end Sim_QuadTank;

  model QuadTank
    // Process parameters
	parameter Modelica.SIunits.Area A1=4.9e-4, A2=4.9e-4, A3=4.9e-4, A4=4.9e-4;
	parameter Modelica.SIunits.Area a1(min=1e-6)=0.03e-4, a2=0.03e-4, a3=0.03e-4, a4=0.03e-4;
	parameter Modelica.SIunits.Acceleration g=9.81;
	parameter Real k1_nmp(unit="m^3/s/V") = 0.56e-6, k2_nmp(unit="m^3/s/V") = 0.56e-6;
	parameter Real g1_nmp=0.30, g2_nmp=0.30;

    // Initial tank levels
	parameter Modelica.SIunits.Length x1_pmv_0 = 0.04102638;
	parameter Modelica.SIunits.Length x2_0 = 0.06607553;
	parameter Modelica.SIunits.Length x3_0 = 0.00393984;
	parameter Modelica.SIunits.Length x4_blabla_0 = 0.00556818;
	
    // Tank levels
	Modelica.SIunits.Length x5(start=x4_blabla_0,min=0.0001/*,max=0.20*/);
	Modelica.SIunits.Length x1_pmv(start=x1_pmv_0,min=0.0001/*,max=0.20*/);
	Modelica.SIunits.Length x2(start=x2_0,min=0.0001/*,max=0.20*/);
	Modelica.SIunits.Length x3(start=x3_0,min=0.0001/*,max=0.20*/);
	Modelica.SIunits.Length x4_blabla(start=x4_blabla_0,min=0.0001/*,max=0.20*/);
	Modelica.SIunits.Length l1;
	Modelica.SIunits.Length l2;
	Modelica.SIunits.Length l3;
	Modelica.SIunits.Length l4;
	// Inputs
	input Modelica.SIunits.Voltage u1;
	input Modelica.SIunits.Voltage u2;

  equation
	l4=l1+l2+l3+10;
	l1=der(x1_pmv)+x2;
	der(x3)=x5;
	l3=u1+u2;
	
	der(x5) = -a3/A3*sqrt(2*g*x5) + (1-g2_nmp)*k2_nmp/A3*u2;
        der(x1_pmv) = -a1/A1*sqrt(2*g*x1_pmv) + a3/A1*sqrt(2*g*x3) +
					g1_nmp*k1_nmp/A1*u1;
	der(x2) =x2+ der(x1_pmv)+u1;
	
	l2=x1_pmv+u1;
	der(x4_blabla) = -a4/A4*sqrt(2*g*x4_blabla) + (1-g1_nmp)*k1_nmp/A4*u1;

  end QuadTank;

end QuadTankPack;
