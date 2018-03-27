
import time
import copy as cp
import sys
import os
import itertools
#import numpy as np

count_A1=0		#Global counters for nodes expanded
count_A2=0
count_BFS=0
count_IDDFS=0

try:	
    import psutil	#Package for computing the memory consumption
except ImportError:		#Try to install requests module if not present
    print("Installing the required 'psutil' module\n")
    os.system('sudo python -m pip install psutil')
import psutil


def astar_heu_1(start,end):
	#A* algorithm using 1st heuristic
	frontier = [[heur_1(start), start]]  #Get the frontier
	expanded = []			     #Generate a new list with more nodes	
	nodes=0
	while frontier:		
		i = 0
		for j in range(1, len(frontier)):
			if frontier[i][0] > frontier[j][0]:	#Check for lower heuristics
				i = j					
		path = frontier[i]
		frontier = frontier[:i] + frontier[i+1:]
		lastnode = path[-1]				#Get the last node 
		if lastnode == end:				#Check for goal state
			break
		if lastnode in expanded: continue		
		for k in p_moves(lastnode):
			if k in expanded: continue
			newpath = [path[0] + heur_1(k) - heur_1(lastnode)] + path[1:] + [k]
			#print 'Heur value........................',heur_2(newpath[-1]), 'at level ' ,len(newpath)
			frontier.append(newpath)		#Add the new path to further processing
			expanded.append(lastnode)
		nodes += 1					#Incerement nodes counter
	print "Expanded nodes:", nodes
	global count_A1
	count_A1=nodes						#Send final nodes generated value using global variable
	print "A* heuristic 1:"
	for i in range(1,len(path)-1):
		print(path[i])					#Print output path

def heur_1(state):
	#Count the number of moved tiles
	moved = 0
	comp = 0
	m = eval(state)
	for i in range(4):
		for j in range(4):
			if m[i][j] != comp:		#Checks if the tile is not at it's goal position
				moved += 1
			comp += 1
	return moved

def astar_heu_2(start,end):
	#A* algorithm using 2nd heuristic
	frontier = [[heur_2(start), start]] 
	expanded = []
	nodes=0
	
	while frontier:
		i = 0
		for j in range(1, len(frontier)):
			if frontier[i][0] > frontier[j][0]:
				i = j
		path = frontier[i]
		frontier = frontier[:i] + frontier[i+1:]
		lastnode = path[-1]
		if lastnode == end:
			break
		if lastnode in expanded: continue
		for k in p_moves(lastnode):
			if k in expanded: continue
			newpath = [path[0] + heur_2(k) - heur_2(lastnode)] + path[1:] + [k]
			#print 'Heur value........................',heur_2(newpath[-1]), 'at level ' ,len(newpath)
			frontier.append(newpath)
			expanded.append(lastnode)
		nodes += 1
	print "Expanded nodes:", nodes
	global count_A2
	count_A2=nodes
	print "A* heuristic 2:"
	for i in range(1,len(path)-1):
		print(path[i])

def heur_2(state):
	#Calculate the Manhattan Distance
	man_distance = 0
	m = eval(state)
	for i in range(4):
		for j in range(4):
			if m[i][j] == 0: continue		#Ignore the blank tile
			man_distance += abs(i - (m[i][j]/4)) + abs(j - (m[i][j]%4));
	return man_distance
	
def p_moves(state):
	#Expands along all the possible moves 
	path = []
	
	mat = eval(state)
	i = 0
	while 0 not in mat[i]: i += 1		 #Go ahead until finding 0
	j = mat[i].index(0); 
	
	if i > 0:
		mat[i][j], mat[i-1][j] = mat[i-1][j], mat[i][j]; #up
		path.append(str(mat))
		mat[i][j], mat[i-1][j] = mat[i-1][j], mat[i][j]; #Go back	
	
	if i < 3:
		mat[i][j], mat[i+1][j] = mat[i+1][j], mat[i][j] #down
		path.append(str(mat))
		mat[i][j], mat[i+1][j] = mat[i+1][j], mat[i][j]
	
	if j > 0:
		mat[i][j], mat[i][j-1] = mat[i][j-1], mat[i][j] #left
		path.append(str(mat))
		mat[i][j], mat[i][j-1] = mat[i][j-1], mat[i][j]
	
	if j < 3:
		mat[i][j], mat[i][j+1] = mat[i][j+1], mat[i][j] #right
		path.append(str(mat))
		mat[i][j], mat[i][j+1] = mat[i][j+1], mat[i][j]
	
	return path
	
	


def breadth_first(start,end):
	
	frontier = [[start]]
	expanded = []
	nodes=0
	while frontier:
		i = 0
		for j in range(1, len(frontier)):			
			if len(frontier[i]) > len(frontier[j]):
				i = j
		path = frontier[i]
		frontier = frontier[:i] + frontier[i+1:]
		lastnode = path[-1]
		if lastnode in expanded: continue
		for k in p_moves(lastnode):			#Expand state
			if k in expanded: continue		#Check for repeated state
			frontier.append(path + [k])
		expanded.append(lastnode)
		nodes += 1
		if lastnode == end: break
	print "Expanded nodes:",nodes
	global count_BFS
	count_BFS=nodes
	print "BFS:"
	for i in range(0,len(path)):
		print(path[i])


def tile(hor,ver):
	
	def expand(state):
	    poss_moves=[]		#Storing all the possible moves
		
	    arow,acol=next((r,c)	  #In-built function for iterations
	    for r,l in enumerate(state)   #Allows us to loop over next() and have an autostateic counter
	    for c,v in enumerate(l) if v==0)   ##Searching for the blank tile position

	    def tile_swap(brow,bcol):
		swapped_blank_tile=cp.deepcopy(state)		#Making a temporary variable for swap 
		swapped_blank_tile[arow][acol],swapped_blank_tile[brow][bcol]=swapped_blank_tile[brow][bcol],swapped_blank_tile[arow][acol]
		return swapped_blank_tile

	    cnt=0	
	    if arow>0:     	        
		poss_moves.append(tile_swap(arow-1,acol))

	    if arow<hor-1:		
		poss_moves.append(tile_swap(arow+1,acol))

	    if acol<ver-1:		
		poss_moves.append(tile_swap(arow,acol+1))

	    if acol>0:			
		poss_moves.append(tile_swap(arow,acol-1))
	    	
	    return poss_moves
	return expand


def iddfs(input,goal_state,expand):
    def dfs(route,level):
            counter=0
            if level==0:			#If input state is the goal node
            	return
            if route[-1]==goal_state:		#Check for the goal node
                return route
            for move in expand(route[-1]):	#Expanding the further nodes
                if move not in route:		#Adding next node if it's not added previously
                    next_route=dfs(route+[move],level-1)
                    global count_IDDFS
		    count_IDDFS+=1
                    if next_route:
                        return next_route	#Added the next node to the current path
    
    for level in itertools.count():		#Condition for Iterative Deepning
        route=dfs([input],level)
       # if level>0:
            	#endtime=time.time()-startTime
	    	#print "Time to solve at level" ,level,":",endtime	    #Time consumed at each state
        if route:
            return route

	
if __name__ == '__main__':
	
	input=([[1,2,3,0],				#input state	
               [4,5,6,7],
               [8,9,10,11],
               [12,13,14,15]])
	
	
	end = ([[0, 1, 2, 3],				#Goal State		
		[4, 5, 6, 7], 
		[8, 9, 10, 11],
		[12, 13, 14, 15]])
	
	try:
		startA1=time.time()
		astar_heu_1(str(input),str(end))
		printA1=time.time()-startA1
		#global count_A1
		memoryA1=count_A1*sys.getsizeof(input)
	
		print "----------------------------------------------------------------------"

		startA2=time.time()
		astar_heu_2(str(input),str(end))
		printA2=time.time()-startA2
		#global count_A2
		memoryA2=count_A2*sys.getsizeof(input)
	
		print "----------------------------------------------------------------------"
	
		startBFS=time.time()
		breadth_first(str(input),str(end))
		printBFS=time.time()-startBFS
		#global count_BFS
		memoryBFS=count_BFS*sys.getsizeof(input)
	
		print "----------------------------------------------------------------------"
	
		startIDDFS=time.time()
		states_path=iddfs(input, end, tile(4,4))
		printIDDFS=time.time()-startIDDFS
		#global count_IDDFS
		print 'Expanded Nodes: ',count_IDDFS
		print 'IDDFS:'
		for i in range(0,len(states_path)-1):	
			print(states_path[i])				#Printing all the states
		print(states_path[len(states_path)-1])
		#global count_IDDFS
		memoryIDDFS=count_IDDFS*sys.getsizeof(input)

		print "-----------------------------------------------------------------------"
	
		print "Time and Memory Consumed: \n"
		print "1. A-Star Heuristic 1 \nTime- ",printA1,' seconds'
		print "Memory: ",memoryA1," \n"	
	
		print "2. A-Star Heuristic 2 \nTime- ",printA2,' seconds'
		print "Memory: ",memoryA2," \n"	
	
		print "3. BFS \nTime- ",printBFS,' seconds'
		print "Memory: ",memoryBFS," \n"	
	
		print "4. IDDFS \nTime- ",printIDDFS,' seconds'
		print "Memory: ",memoryIDDFS," \n"	
	
	
	except MemoryError:					#Memory out of bounds exception
		print('The program ran out of memory')		
		
	
