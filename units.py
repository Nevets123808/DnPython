import function
import math
import pygame
class Creature:

	alive = True
	pos = [0,0]
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
	def DrawCreature(self,screen):
		surf = pygame.Surface((16,16))
		surf.fill(self.colour)
		rect = surf.get_rect()
		screen.blit(surf,(self.pos[0]*16,self.pos[1]*16))

class Weapon:
	def __init__(self, statList):
		self.name = statList[0]
		self.diceNum = statList[1]
		self.damDice = statList[2]
