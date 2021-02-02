import pygame

class TileMap:
	def __init__(self,width,height):
		self.map = []
		for i in range(width):
			self.map.append([])
			for ii in range(height):
				if( i == 0 or i == (width-1) or ii == 0 or ii == (height-1)):
					self.map[i].append(Tile("Wall.png", False))
				else:
					self.map[i].append(Tile())
	def getTile(self,pos):
		return self.map[int(pos[0])][int(pos[1])]

	def draw(self,screen):
		for i in range(len(self.map)):
			for ii in range(len(self.map[i])):
				self.map[i][ii].draw(screen, [i,ii])
class Tile:
	def __init__(self,terr = "Ground.png", passable = True):
		self.terrain = Terrain(terr, passable)
		self.entity = None

	def clearEntity(self):
		self.entity = None

	def draw(self,screen, pos):
		self.terrain.draw(screen, pos)
		if not self.entity == None:
			self.entity.draw(screen)

class Terrain:
	def __init__(self, img ="Ground.png", passable = True):
		self.img = pygame.image.load(img)
		self.passable = passable

	def draw(self,screen,pos):
		screen.blit(self.img,(pos[0]*64,pos[1]*64))
def main():
	pygame.init()
	SCREENWIDTH =  640
	SCREENHEIGHT = 480
	screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
	clock = pygame.time.Clock()
	tileMap = TileMap(8,8)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill((255,255,255))
		tileMap.draw(screen)
		pygame.display.update()
	pygame.quit()

if __name__ == "__main__":
	main()
