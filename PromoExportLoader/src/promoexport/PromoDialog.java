package promoexport;
import java.awt.Dimension;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;

import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import net.n3.nanoxml.*;


public class PromoDialog extends JDialog {
	JTextField inputFileContainer;
	JTextField modelNameContainer;
	JTextField regExpContainer;
	JTextField outPutFileContainer;
	ExportInvoker owner;
	String inputfilepath="null";
	public PromoDialog(JFrame parent, String title,ExportInvoker owner){
		super(parent,title,true);
		
	    if (parent != null) {
	        Dimension parentSize = parent.getSize(); 
	        Point p = parent.getLocation(); 
	        setLocation(p.x + parentSize.width / 4, p.y + parentSize.height / 4);
	      }
	    
	    getContentPane().setLayout(new BoxLayout(this.getContentPane(), BoxLayout.Y_AXIS));
	    getContentPane().add(this.getInputFilePane());
	    getContentPane().add(this.getModelSpecPane());
	    getContentPane().add(this.getRegExpPane());
	    getContentPane().add(this.getOutPutPane());
	    getContentPane().add(this.getOkCancelPane());
	    this.owner=owner;
		pack(); 
	    setVisible(true);
	}
	public JPanel getInputFilePane(){
		JPanel toReturn=new JPanel();
		
		toReturn.add(new JLabel("Input"));
		inputFileContainer=new JTextField("Välj fil",80);
		inputFileContainer.setEnabled(false);
		toReturn.add(inputFileContainer);
		
		final JButton openFileButton=new JButton("Open file");
		
		openFileButton.addActionListener(new ActionListener() {
		  public void actionPerformed(ActionEvent evt) {
		    // ... called when button clicked
			  inputFileContainer.setText("lool");
			  final JFileChooser filePick = new JFileChooser();
			  ModelicaFileFilter filter = new ModelicaFileFilter(false); 
			
		
			  
			    filePick.setFileFilter(filter);
	            filePick.showOpenDialog(openFileButton);

	          
	                // Open an input stream
	              File f=filePick.getSelectedFile();
	              inputFileContainer.setText(f.getAbsolutePath());
	         
		  }
		});
		
		toReturn.add(openFileButton);
		
		
		
		return toReturn;
		
	}
	public JPanel getModelSpecPane(){
		JPanel toReturn=new JPanel();
		toReturn.add(new JLabel("Model name"));
		modelNameContainer=new JTextField("PackageName.ModelName",80);
		modelNameContainer.addActionListener(new ActionListener() {
			  public void actionPerformed(ActionEvent evt) {
			    // ... called when button clicked
				 
		              System.out.println(modelNameContainer.getText());
		         
			  }
			});
		
		
		modelNameContainer.setEnabled(true);
		toReturn.add(modelNameContainer);
		
		return toReturn;
	}
	public JPanel getRegExpPane(){
		JPanel toReturn=new JPanel();
		toReturn.add(new JLabel("regexp"));
		regExpContainer=new JTextField("_pmv",80);

		
		
		toReturn.add(regExpContainer);
		
		return toReturn;
	}
	public JPanel getOutPutPane(){
		JPanel toReturn=new JPanel();
		toReturn.add(new JLabel("OutputPath"));
		outPutFileContainer=new JTextField("C:\\ProMoVis\\emitted\\",80);
		outPutFileContainer.setEnabled(false);
		final JButton openFileButton=new JButton("Open File");
		
		
		openFileButton.addActionListener(new ActionListener() {
		  public void actionPerformed(ActionEvent evt) {
		    // ... called when button clicked
			  outPutFileContainer.setText("lool");
			  final JFileChooser filePick = new JFileChooser();
			  
			//  ModelicaFileFilter filter = new ModelicaFileFilter(true); 
			
			   	filePick.setCurrentDirectory(new java.io.File("."));
			    filePick.setDialogTitle("Open File");
			    filePick.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
			    filePick.setAcceptAllFileFilterUsed(false);
	                // Open an input stream
			    filePick.showOpenDialog(openFileButton);
	              File f=filePick.getSelectedFile();
	              outPutFileContainer.setText(f.getAbsolutePath());
	         
		  }
		});
		
		
		
		
		
		outPutFileContainer.setEnabled(true);
		toReturn.add(outPutFileContainer);
		toReturn.add(openFileButton);
		return toReturn;
	}
	public JPanel getOkCancelPane(){
		JPanel toReturn=new JPanel();
		
		final JButton okButton=new JButton("OK");
		
		okButton.addActionListener(new ActionListener() {
		  public void actionPerformed(ActionEvent evt) {
		    // ... called when button clicked
			  dispose();
			  if(validInput()){
				  String inputFiledir=getXML();
				  owner.InputFileCreated(inputFiledir, getOutPutFilePath(),PromoDialog.this);
				  
			  }else{
				  
			  }
		  }
		});
		
		final JButton cancelButton=new JButton("Cancel");
		
		okButton.addActionListener(new ActionListener() {
		  public void actionPerformed(ActionEvent evt) {
		    // ... called when button clicked
			  dispose();
		  }
		});

		
		toReturn.add(cancelButton);
		toReturn.add(okButton);
		
		return toReturn;
	}
	public boolean validInput(){
		return true;
	}
	String getXML(){
		//"The standard library was messy, and jdom would be another dependency, so change this to the library for xml handling that promovis uses whenever."
		IXMLElement root=new XMLElement("root");
		IXMLElement filepath = root.createElement("filepath");
		root.addChild(filepath);
		filepath.setContent(this.inputFileContainer.getText());
		
		IXMLElement model= root.createElement("model");
		root.addChild(model);
		model.setContent(this.modelNameContainer.getText());
		
		IXMLElement mpattern = root.createElement("mpattern");
		root.addChild(mpattern);
		mpattern.setContent(this.regExpContainer.getText());
		
		IXMLElement outpathxml = root.createElement("outputpath");
		root.addChild(outpathxml);
		outpathxml.setContent(this.getOutPutFilePath());
		
		IXMLElement outpathpmv = root.createElement("pmvoutputpath");
		root.addChild(outpathpmv);
		outpathpmv.setContent(this.outPutFileContainer.getText()+"outputfile.pmv");
		
		try {
			String writeDir=this.getInputFilePath();
			System.out.println(writeDir);
			FileWriter fstream = new FileWriter(writeDir);
			XMLWriter writer = new XMLWriter(fstream);
			writer.write(root, true);
			fstream.close();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
	
		//System.out.println(root.);
		return this.getInputFilePath();
	}
	String getOutPutFilePath(){
		return this.outPutFileContainer.getText()+"outputfile.xml";
		
	}
	String getInputFilePath(){
		return System.getProperty("user.dir")+"\\inputfile.xml";
	}
}
