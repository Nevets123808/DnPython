class thing:
	def __init__(self,pos):
		self.pos = pos

def gridLocate(pos,grid):
	return grid[pos[1]][pos[0]]

def gridChangeValue(pos,grid,value):
	grid[pos[1]][pos[0]] = value

grid = []
gridWidth = 8
gridHeight = 8
for i in range(gridHeight):
	grid.append([])
	for ii in range(gridWidth):
		grid[i].append(None)
	print(grid[i])

gridChangeValue([5,4],grid,"You found me!")
print (gridLocate([5,4],grid))
print (gridLocate([4,5],grid))
