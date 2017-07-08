# Vass Peter @ BME FRT 2017

# this  script returns the optimal solution to the paperrace game. 
# Worst case time complexity of the algo is O(n^3)

# dependencies are: numpy, scipy, matplotlib 
#	Hint: download these with pip


from scipy.misc import imread,imshow
import numpy as np
import math as ma


from collections import deque



import matplotlib as mp
mp.use('TkAgg')  # to use tkinter gui to show plot
import matplotlib.pyplot as plt
import matplotlib.image as pimg


# currently only checks if dst is on the track. schould be made to check intersections 
def isValid(dst=[0,0], src=[0,0]):
	if dst[0]>=track.shape[0] or dst[1]>=track.shape[1]:
		return False
	if dst[0]<0 or dst[1]<0:
		return False
	
	return (track[dst[0],dst[1]] > 0)
	
# is point p on the end zone of the track?
def isEnd(p=[0,0]):
	return (track[p[0],p[1]] == 3)
	
	



R=[255,0,0]
G=[0,255,0]
B=[0,0,255]


map="map2.bmp"

# raw image data
trackRaw=imread(map)

# track image for plot
trackPlot=plt.imshow(pimg.imread(map))

#simplified representation of the track
track=np.zeros(trackRaw.shape[0:2])
startPos=[-1,-1]

for i in range(track.shape[0]):
	for j in range(track.shape[1]):
		# the track is black	
		if (trackRaw[i,j]==[0,0,0]).all():
			track[i,j]=1
		# start position is a green pixel
		if (trackRaw[i,j]==G).all():
			track[i,j]=2
			
			if startPos == [-1,-1]:
				startPos=[i,j]
				
				print("startPos: [{}, {}]".format(i,j))
			else:
				print("Error! Multiple starting positions.")
		#stop position is any red pixel
		if (trackRaw[i,j]==R).all():
			track[i,j]=3





# graph data structure. This is a "list of list". First two dimensions are of the same size as the map. The third dimension is used as a list for each cell to hold the incoming states
g=[[[] for i in range(track.shape[1])] for i in range(track.shape[0])]


# g[i,j] contains every posibble choice of direction
dir=[	[0,0],
		[1,0],[0,1],[1,1],
		[-1,0],[0,-1],[-1,-1],
		[1,-1],[-1,1]
	]


g[startPos[0]][startPos[1]].append([0,0,0,0]) # we start with velocity of 0,0 and delta of 0,0



q=deque()
q.append([startPos,[0]*2]) # classic queue for BFS


stop=False

# storing the daa of the "winning" move
stopPos=[]
stopVel=[]
stopOrd=0

while(q and not stop):
	cur=q.popleft()
	# consider all posibble directions
	for i in range(len(dir)):
		newVel=np.add(dir[i],cur[1]).tolist()
		newPos=np.add(newVel,cur[0]).tolist()
		
		if isValid(newPos):
			if(isEnd(newPos) and newVel[1]>=0): # this is a hack, write good checking function
				stop=True
				
				stopPos=newPos
				stopVel=newVel
				stopDif=dir[i]
				
				print("stopPos: ",newPos,newVel)
				break
			else:
				# search if state allready exists
				found=False;
				for v in g[newPos[0]][newPos[1]]:
					if v[:2]==newVel:
						found=True
						break
				
				if not found:
					g[newPos[0]][newPos[1]].append(newVel+dir[i])
					q.append([newPos,newVel])
					
					#print(newPos,newVel)
					
#backtrack from the last move to get reversed list of solution

sol=[]

curPos=stopPos
curVel=stopVel
curDif=stopDif

while curPos!=startPos:
	sol.append(curDif)

	curPos=np.subtract(curPos,curVel).tolist()
	curVel=np.subtract(curVel,curDif).tolist()
	
	# find curVel in g, so that curDiff can be updated
	for n in g[curPos[0]][curPos[1]]: # check every node with current coord
		
		if curVel==n[:2]:
			curDif=n[2:]
			break			
sol.append(curDif)

	
print("\n\nSolution:")	
for i in reversed(sol[:-1]):
	print(i)


# plotting. This restores the speed vectors for each turn and draws it on the image of the map
drawPos=startPos
drawPosOld=startPos
vel=np.zeros(2)
col='b'
for i in reversed(sol[:-1]):
	vel=np.add(vel,i)
	
	tPos=drawPos
	drawPos=np.add(drawPos,vel)
	drawPosOld=tPos
	
	plt.plot([drawPosOld[1], drawPos[1]],[drawPosOld[0], drawPos[0]], color=col, linestyle='-', linewidth=1)
	
	if col=='b':
		col='y'
	else:
		col='b'
		
plt.show()
	
	
	








		
		
		
		
		
		
		
		
		
		
		
		
		
		