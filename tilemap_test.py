import pygame
import function
class TileMap:
	def __init__(self,width,height):
		self.map = []
		for i in range(width):
			self.map.append([])
			for ii in range(height):
				if( i == 0 or i == (width-1) or ii == 0 or ii == (height-1)):
					self.map[i].append(Tile((i,ii),"Wall.png", False))
				else:
					self.map[i].append(Tile((i,ii)))

	def getTile(self,pos):
		return self.map[int(pos[0])][int(pos[1])]

	def checkClick(self,pos):
		for row in self.map:
			for tile in row:
				if tile.rect.collidepoint(pos):
					return tile
		return None

	def clearChecks(self):
		for row in self.map:
			for tile in row:
				tile.clearChecks()

	def refreshChecks(self,unit):
		self.clearChecks()
		for row in self.map:
			for tile in row:
				tile.checkAttack(unit)
				tile.checkMove(unit)

	def draw(self,screen):
		for row in self.map:
			for tile in row:
				tile.draw(screen)

	def clearEntities(self):
		for  row in self.map:
			for tile in row:
				tile.clearEntity()
class Tile:
	def __init__(self,pos,terr = "Ground.png", passable = True):
		self.pos = pos
		rect = (pos[0]*64,pos[1]*64,64,64)
		self.rect = pygame.Rect(rect)
		self.terrain = Terrain(terr, passable)
		self.entity = None
		self.overlay = None
		self.moveCheck = False
		self.attackCheck = False

	def clearEntity(self):
		self.entity = None

	def clearChecks(self):
		self.overlay= None
		self.moveCheck = False
		self.attackCheck = False

	def checkMove(self, unit):
		if function.dist(self.pos, unit.pos) <= unit.speed-unit.moveCount and self.terrain.passable and not self.entity:
			self.overlay = (255,255,0)
			self.moveCheck = True

	def checkAttack(self,unit):
		if function.dist(self.pos, unit.pos) <= (unit.speed-unit.moveCount)+unit.weapon.range and self.terrain.passable and not self.entity == unit:
			self.overlay = (255,0,0)
			self.attackCheck = True

	def draw(self,screen):
		self.terrain.draw(screen, self.pos)
		if self.entity:
			self.entity.draw(screen)
		if self.overlay:
			s= pygame.Surface((64,64))
			s.set_alpha(25)
			s.fill(self.overlay)
			screen.blit(s,self.rect)

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
	colourActive = pygame.Color(255,255,0,a = 25)
	screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
	clock = pygame.time.Clock()
	tileMap = TileMap(8,8)
	tileMap.getTile((4,4)).overlay = colourActive

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
