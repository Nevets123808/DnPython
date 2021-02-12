import function
from function import *
import math
import pygame
from pygame.locals import *
import pygame_reg
class Creature:

	alive = True
	pos = [1,1]
	init = 0
	speed = 6
	acted = False
	Turn = False
	text = None

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

	def __init__(self, statList, img = None):

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
		self.moveCount = 0
		if img:
			self.img = pygame.image.load(img)
		else:
			self.img = None

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

	def draw(self,screen):
		if self.img:
			screen.blit(self.img,(self.pos[0]*64,(self.pos[1]-1)*64))
		else:
			surf = pygame.Surface((16,16))
			surf.fill(self.colour)
			rect = surf.get_rect()
			screen.blit(surf,(self.pos[0]*64,self.pos[1]*64))

class Player(Creature):
	def __init__(self, statList, img = None):
		self.abilityNames = []
		self.abilities = []
		self.menu = pygame_reg.Menu((0,0))
		self.menu_active = False
		super().__init__(statList, img)

	def GetAbility(self, ability):
		self.abilities.append(ability)
		self.abilityNames.append(ability.name)

	def move(self, actor, target, stack):
		dist = function.dist(actor.pos, target.pos)
		actor.moveCount += dist
		stack.createAction(moveStep, actor, target, dist)

	def clearMenu(self):
		self.menu.clearButtons()
		self.menu_active = False
	def PopulateMenu(self,tile, stack):
		self.menu.clearButtons()
		self.menu.rect.left = tile.pos[0]*64
		self.menu.rect.top = tile.pos[1]*64
		check = False
		if tile.moveCheck: 
			check = True
			self.menu.addButton("Move", self.move,self,tile, stack)
		if check:
			self.menu_active = True

class Weapon:
	def __init__(self, statList):
		self.name = statList[0]
		self.diceNum = statList[1]
		self.damDice = statList[2]
		self.range = statList[3]
