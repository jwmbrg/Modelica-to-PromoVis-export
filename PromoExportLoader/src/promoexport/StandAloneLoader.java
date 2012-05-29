package promoexport;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import javax.swing.JFrame;

public class StandAloneLoader {
	public static String _BATLOCATION="JModelica.bat";
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		PromoDialog theDialog=new PromoDialog(new JFrame(),"Ladda ",new ExportInvoker(){

			@Override
			public void InputFileCreated(String inputFilePath,
					String outputFilePath, PromoDialog dialog) {
				// TODO Auto-generated method stub
				System.out.println("Should run python with: "+inputFilePath+" the result should then be collected from "+outputFilePath);
				
				
				
		        try
		        {
		            Runtime r = Runtime.getRuntime();
		            Process p = r.exec("JModelica.bat "+inputFilePath);
		            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
		            p.waitFor();
		            String line = "";
		            while (br.ready())
		                System.out.println(br.readLine());

		        }
		        catch (Exception e)
		        {
				String cause = e.getMessage();
				if (cause.equals("python: not found"))
					System.out.println("No python interpreter found.");
		        }
		        
		        System.out.println("file successfully created "+outputFilePath);
			}
			
		});
		
	}	

}
