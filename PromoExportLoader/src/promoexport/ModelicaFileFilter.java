package promoexport;

import java.io.File;

import javax.swing.filechooser.FileFilter;


public class ModelicaFileFilter extends FileFilter {
	boolean dirOnly=false;
	ModelicaFileFilter(boolean dirOnly){
		this.dirOnly=dirOnly;
		
	}	public boolean accept(File arg0) {
		// TODO Auto-generated method stub
	  
	      if (arg0.getName().toLowerCase().endsWith(".mo")) return true &&(!dirOnly); else return arg0.isDirectory();
	    
	    
	}

	@Override
	public String getDescription() {
		// TODO Auto-generated method stub
		return "Modelica files *.mo";
	}

}
