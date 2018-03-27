
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.util.Scanner;

public class CS411_15puzzle extends VirtualMachineError {					

	private static final long serialVersionUID = 4307774437766027133L;
	final long startTime=System.currentTimeMillis();                       
	//Saving the starting time of the program  
	final long beforeUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();  
	//Saving the initial memory consumed 

	Queue<String> q=new LinkedList<String>();              
	//Queue used to add new nodes and search through them using BFS 
	Map<String,Integer> m=new HashMap<String,Integer>();	
	/*HashMap used to store the states with their level 
	 * Used to get the level of a state and checking for repeated states
	 */
	StringBuilder stateHistory = new StringBuilder();	
	//Variable string for storing history of moves	

	public static void main(String[] args) {
	
		Scanner scan=new Scanner(System.in);
		System.out.println("Guide for input--> Represent the blank with 'X' & ABCDEF for 10-15\n");
		System.out.print("Enter the input state of the 15-puzzle : ");
		String inputString=scan.nextLine();							
		//Getting the input....Blank represented by 'X'
		scan.close();
	
		/*   
		 * Sample inputs
	 	 *		String inputString="123456789ABCDEXF";	(Simple Input)
		 *		String inputString="517392B4D6F8AXEC";	(Complex Input)
		 *		String inputString="XABCDEF123456789";	(Runs out of memory)
		 */		
		
		CS411_15puzzle game=new CS411_15puzzle();		    //New instance creation
		game.add(inputString,0,"");              	    
		//Adding the input state as root node with level 0
		
		//BFS code
		while(game.q.peek()!=null)						
		{												//Read the current node
				game.upBlank(game.q.peek());			
				//Move the blank up and store new state in the Queue
				game.downBlank(game.q.peek());		
				//Move the blank down and store new state in the Queue
				game.leftBlank(game.q.peek());		
				//Move the blank left and store new state in the Queue
				game.rightBlank(game.q.remove());		
				/* Move the blank up and store new state in the Queue
				 * Also, remove the current node from Queue as it has been expanded completely
				 */	
		}											
		System.out.println("Solution doesn't exist");	
	}	   //main function ends
		
	
		private void add(String str, int n,String action)		//Adding new state
		{
			if(!m.containsKey(str))								
				//CHECKING FOR REPEATED STATES IN THE HASHMAP	
			{
				m.put(str,n);									
				//Adding new state in the HashMap
				q.add(str);										
				//Adding new states in the Queue
				stateHistory.append(str+"\t"+action+"\n");		
				//Add the new state in the buffer for printing later
			}
		}
		
/*
 * The below methods find the current location of the blank (We have represented the blank as "X").
 * The blank is moved if only it can be moved in the puzzle and the new state is stored in the Queue and HashMap and expanded later.
 * Every time we create a new state, we check if the state is the goal state and exit the program.  		
 */
		/*private int numDisplacedTiles(String str)
		{
			int count=0;
			
			for(int i=0;i<9;i++)	
			{	
				System.out.println((int)str.charAt(i));
				if((int)str.charAt(i) != 49+i)
				{
					count++;
				}
			}
			
			for(int i=9,inc=0 ; i<15 ; i++,inc++)
			{
				System.out.println((int)str.charAt(i));
				int a=(int)str.charAt(i);
				if(a!=(65+inc))
				{
					count++;
				}
				
			}
			
			return count;
		}*/
		
		
		private void upBlank(String str) 						
		//Current state as input through the function parameter
		{
			try
			{
				int blank=str.indexOf("X"); 
				//Search for the blank
				if(blank>3)	
				//Check if the blank is not in the uppermost row
				{
					//Create a string with the new state when the blank is moved up	
					String resState=str.substring(0, blank-4)+"X"+str.substring(blank-3, blank)+str.charAt(blank-4)+str.substring(blank+1); 

					add(resState,m.get(str)+1,"UP");		
					/*Call the add function with the new generated state 
					 * and with one additional depth value than its parent
					 */ 
		
					if(resState.equals("123456789ABCDEFX"))	
					//Check if the new state is the goal state
					{
						System.out.println("Solution states are: \n"+ stateHistory);
						//Printing the entire execution history till the goal state 
						System.out.println("Goal state found at level: "+ m.get(resState));		
						//Checking the depth of the goal state
						
						long endTime=System.currentTimeMillis();			
						//Calculating the end time of program
						long totalTime=(endTime-startTime);					
						//Time of execution of program
						System.out.println("Time taken: "+totalTime+" millliseconds");
	
						long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
						//Memory utilized at current step
						long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;								
						//Total memory consumed	by the program	
						System.out.println("Total Memory Used: "+actualMemUsed+" kB");
						
						System.exit(0);				
						//Exit as the goal state has been found
					}
				}
			}
			catch(OutOfMemoryError ex)					
			/*
			 * Exception handling when JVM cannot allocate an object because it is out of memory, 
			 * and no more memory could be made available by the garbage collector
         	 */
			{
				System.out.println("System ran out of memory at level "+ m.get(str));	
				//Getting current depth through the HashMap
				
				long endTime=System.currentTimeMillis();
				long totalTime=(endTime-startTime);
				System.out.println("Time taken: "+totalTime+" milliseconds");

				long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
				long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
				System.out.println("Total Memory Used: "+actualMemUsed+" kB");
				System.exit(1);													
				/*
				 * Exit the program with the handled exception
				 * The program keeps catching the same exception if not exited
				 */
			}
		}
		
		
		private void downBlank(String str) 
		{
			try
			{
				int blank=str.indexOf("X");
				if(blank<12)										
				//Check if the blank is not in the lower-most row
				{
					String resState=str.substring(0, blank)+str.charAt(blank+4)+str.substring(blank+1, blank+4)+"X"+str.substring(blank+5);
					add(resState,m.get(str)+1,"DOWN");
					if(resState.equals("123456789ABCDEFX"))
					{
						System.out.println("Solution states are: \n"+ stateHistory);
						System.out.println("Goal state found at level: "+ m.get(resState));
						
						long endTime=System.currentTimeMillis();
						long totalTime=(endTime-startTime);
						System.out.println("Time taken: "+totalTime+" milliseconds");
	
						long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
						long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
						System.out.println("Total Memory Used: "+actualMemUsed+" kB");
						
						System.exit(0);
					}
				}
			}	
			catch(OutOfMemoryError ex)
			{
				System.out.println("System ran out of memory at level "+ m.get(str));
				long endTime=System.currentTimeMillis();
				long totalTime=(endTime-startTime);
				System.out.println("Time taken: "+totalTime+" milliseconds");

				long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
				long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
				System.out.println("Total Memory Used: "+actualMemUsed+" kB");
				System.exit(1);
			}
		}

	
		private void leftBlank(String str) 
		{
			try
			{
				int blank=str.indexOf("X");
				if(blank!=0&&blank!=4&&blank!=8&&blank!=12)		
				//Check if the blank is not in the left-most row
				{
					String resState=str.substring(0, blank-1)+"X"+str.charAt(blank-1)+str.substring(blank+1);
					add(resState,m.get(str)+1,"LEFT");
					if(resState.equals("123456789ABCDEFX"))
					{
						System.out.println("Solution states are: \n"+ stateHistory);
						System.out.println("Goal state found at level: "+ m.get(resState));
						
						long endTime=System.currentTimeMillis();
						long totalTime=(endTime-startTime);
						System.out.println("Time taken: "+totalTime+" milliseconds");
	
						long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
						long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
						System.out.println("Total Memory Used: "+actualMemUsed+" kB");
						
						System.exit(0);
					}
				}
			}	
			catch(OutOfMemoryError ex)
			{
				System.out.println("System ran out of memory at level "+ m.get(str));
				long endTime=System.currentTimeMillis();
				long totalTime=(endTime-startTime);
				System.out.println("Time taken: "+totalTime+" milliseconds");

				long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
				long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
				System.out.println("Total Memory Used: "+actualMemUsed+" kB");
				System.exit(1);
				
			}
		}
		
		private void rightBlank(String str) 
		{
			try
			{
				int blank=str.indexOf("X");
				if(blank!=3&&blank!=7&&blank!=11&&blank!=15)				
				//Check if the blank is not in the right-most row
				{
					String resState=str.substring(0,blank)+str.charAt(blank+1)+"X"+str.substring(blank+2);
					add(resState,m.get(str)+1,"RIGHT");
					if(resState.equals("123456789ABCDEFX"))
					{
						System.out.println("Solution states are: \n"+ stateHistory);
						System.out.println("Goal state found at level: "+ m.get(resState));
						
						long endTime=System.currentTimeMillis();
						long totalTime=(endTime-startTime);
						System.out.println("Time taken: "+totalTime+" milliseconds");
	
						long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
						long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
						System.out.println("Total Memory Used: "+actualMemUsed+" kB");
						
						System.exit(0);
					}
				}
			}
			catch(OutOfMemoryError ex)
			{
				System.out.println("System ran out of memory at level "+ m.get(str));
				long endTime=System.currentTimeMillis();
				long totalTime=(endTime-startTime);
				System.out.println("Time taken: "+totalTime+" milliseconds");

				long afterUsedMem=Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
				long actualMemUsed=(afterUsedMem-beforeUsedMem)/1024;
				System.out.println("Total Memory Used: "+actualMemUsed+" kB");
				System.exit(1);
			}
		}
}
