
import time
import copy as cp
import sys
import os
import itertools

try:
    import psutil	#Package for computing the memory consumption
except ImportError:		#Try to install requests module if not present
    print("Installing the required 'psutil' module\n")
    os.system('sudo python -m pip install psutil')
import psutil

def tile(hor,ver):
	def expand(state):
	    poss_moves=[]		#Storing all the possible moves

	    arow,acol=next((r,c)	  #In-built function for iterations
	    for r,l in enumerate(state)   #Allows us to loop over next() and have an automatic counter
	    for c,v in enumerate(l) if v==00)   ##Searching for the blank tile position

	    def tile_swap(brow,bcol):
		swapped_blank_tile=cp.deepcopy(state)		#Making a temporary variable for swap 
		swapped_blank_tile[arow][acol],swapped_blank_tile[brow][bcol]=swapped_blank_tile[brow][bcol],swapped_blank_tile[arow][acol]
		return swapped_blank_tile


	    if arow>0:     	        #Blank up
		poss_moves.append(tile_swap(arow-1,acol))

	    if arow<hor-1:		#Blank down
		poss_moves.append(tile_swap(arow+1,acol))

	    if acol<ver-1:		#Blank right
		poss_moves.append(tile_swap(arow,acol+1))


	    if acol>0:			#Blank left
		poss_moves.append(tile_swap(arow,acol-1))

	    return poss_moves
	return expand


def iddfs(puzzle,goal_state,expand):
    def dfs(route,level):
            if level==0:			#If input state is the goal node
            	return
            if route[-1]==goal_state:		#Check for the goal node
                return route
            for move in expand(route[-1]):	#Expanding the further nodes
                if move not in route:		#Adding next node if it's not added previously
                    next_route=dfs(route+[move],level-1)
                    if next_route:
                        return next_route	#Added the next node to the current path
    
    print "\nTime required at each level-"	
    for level in itertools.count():		#Condition for Iterative Deepning
        route=dfs([puzzle],level)
        if level>0:
            	endtime=time.time()-startTime
	    	print "Time to solve at level" ,level ,"  : ",endtime	    #Time consumed at each state
        if route:
            return route


if __name__=='__main__':

    startTime=time.time()			#Start Time

    inputState=[[1,2,3,4],			#Input State where blank is denoted by '0'
                 [10,9,6,8],
                 [5,0,7,12],
                 [13,14,11,15]]

   # inputState=[[1,2,3,4],
    #           [5,6,7,8],
     #          [9,10,11,12],
      #         [13,14,15,0]]
	

    goalState=[[1,2,3,4],			#Goal State
               [5,6,7,8],
               [9,10,11,12],
               [13,14,15,0]]

 
    	
    try:	
	    states_path=iddfs(inputState, goalState, tile(4,4))		#Call the ID-DFS function
	    #time=time.time()-startTime
	    if states_path==None:					#If no path received
		print("Solution doesn't exist for the input")
	    else:
	    	print '\nThe states path is: \n'
		for i in range(0,len(states_path)-1):
		    print(states_path[i])				#Printing all the states
		print(states_path[len(states_path)-1])
   	
    except MemoryError:		#Memory out of bounds
    	print('The program ran out of memory')
 

    print '\nSoultion found at level: ', len(states_path)
    finaltime=time.time()-startTime				#End Time
    print '\nThe final time consumed in seconds: ', finaltime
    process=psutil.Process(os.getpid())
    memory=process.memory_info().rss/1000000			#Total memory consumed
    print "\nMemory used : ", memory," mb\n"			

