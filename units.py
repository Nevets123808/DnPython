import function
import math
import pygame
from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	K_RETURN,
	K_SPACE,
	KEYDOWN,
	QUIT,
)
class Creature:

	alive = True
	pos = [1,1]
	init = 0
	speed = 6

	def StatMod(self,stat):
		return math.floor((stat-10)/2)

	#By using a method, we can update modifiers quickly.
	def GetMod(self):
		self.strMod = self.StatMod(self.str)
		self.dexMod = self.StatMod(self.dex)
		self.conMod = self.StatMod(self.con)
		self.intMod = self.StatMod(self.int)
		self.wisMod = self.StatMod(self.wis)
		self.chaMod = self.StatMod(self.cha)

	def __init__(self, statList):

		#initialise name
		self.name = statList[0]

		#initialise  ability scores
		self.str = statList[1]
		self.dex = statList[2]
		self.con = statList[3]
		self.int = statList[4]
		self.wis = statList[5]
		self.cha = statList[6]

		self.GetMod()

		self.AC = 10 + self.dexMod
		self.HP = statList[7]

		self.colour = (0,0,0)
	def GetHP(self,hitDie):
		self.hitDie = hitDie
		self.HP = hitDie + self.conMod
	def GetWeapon(self, weaponStat):
		self.weapon = Weapon(weaponStat)

	def SetInitiative(self):
		self.init = function.Dice(1,20)+self.dexMod

	def Move(self, MoveVector):
		for i in range(len(self.pos)):
			self.pos[i] += MoveVector[i]
	def Draw(self,screen):
		surf = pygame.Surface((16,16))
		surf.fill(self.colour)
		rect = surf.get_rect()
		screen.blit(surf,(self.pos[0]*64,self.pos[1]*64))

class Player(Creature):
	pass

class Weapon:
	def __init__(self, statList):
		self.name = statList[0]
		self.diceNum = statList[1]
		self.damDice = statList[2]
class Tile:
	def __init__(self, terrain = "Ground"):
		self.terrain = terrain
		self.entity = None

	def ClearEntity(self):
		self.entity = None

	def Draw(self,screen):

		if not type(self.entity)== None:
			self.entity.Draw(screen)

class TileMap:
	def __init__(self, Height, Width):
		self.map = []
		for i in range(width):
			self.map.append([])
			for ii in range(height):
				self.map[i].append(Tile())

	def GetTile(self, pos):
		return self.map[pos[0]][pos[1]]


	def Draw(self, screen):
		for i in self.map:
			for ii in self.map[i]:
				ii.Draw(screen)
