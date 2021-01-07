import function
import units

import random
import math

import pygame
import pygame_reg as regs

#Import from pygame.locals for easier access to key coordinates
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
pygame.init()
class EntityList:
	def __init__(self):
		self.list =[]

	def addEntity(self, entity):
		self.list.append(entity)

	def draw(self, screen):
		screen.fill((255,255,255))
		for i in self.list:
			if type(i) == units.Creature:
				i.DrawCreature(screen)

	def maxInit(self):
		max = 0
		for i in self.list:
			if i.init > max: max = i.init
		return max

	def checkPos(self, pos):
		for i in self.list:
			if i.pos == pos:
				return i
class InfoBox:
	def __init__(self, label, x,y,w,h):
		half_width = w
		self.label = regs.TextObject(x,y,half_width,h, label)
		self.text = regs.TextObject(x+half_width,y,half_width,h)
	def draw(self,screen):
		self.label.draw(screen)
		self.text.draw(screen)

def SpawnCreature(name,weapon):
	enemy = units.Creature(creature[name])
	enemy.GetWeapon(weapons[weapon])
	enemy.SetInitiative()
	enemy.pos = [random.randint(0,7),random.randint(0,7)]
	enemy.colour = (0,125,0)
	return enemy

def basicAI(enemy):
	target = function.subPos(player.pos,enemy.pos)
	if not target[0] == 0:
		movePos = [(target[0]/abs(target[0])),0]
	elif not target[1] == 0:
		movePos =[0,(target[1]/abs(target[1]))]
	else:
		enemy.Turn = False
		return
	targetPos = function.addPos(enemy.pos,movePos)
	check = eList.checkPos(targetPos)

	if type(check) == units.Creature and enemy.attackCount < 1:
		enemy.inactive = 0
		logBox.text=function.Attack(enemy,player)[2]
		hpBox.text.text = str(player.HP)
		enemy.attackCount += 1
	elif enemy.moveCount < enemy.speed and check == None:
		inactive = 0
		enemy.Move(movePos)
		enemy.moveCount += 1
	elif enemy.inactive >= 3:
		enemy.Turn = False
		print("End of Turn")
	else:
		enemy.inactive+=1 
		print("inactive")

SCREENWIDTH = 1024
SCREENHEIGHT = 700

HALFWIDTH = math.floor(SCREENWIDTH/2)
HALFHEIGHT = math.floor(SCREENHEIGHT/2)

screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
gameView = pygame.Surface((SCREENWIDTH-20,SCREENHEIGHT-148))
clock = pygame.time.Clock()

#initialise the entity grid
mapHeight = 8
mapWidth = 8
eList = EntityList()


#create some basic creatures and weapons
creature = function.LoadDict("creatures.dat")
creature.update({"Gary":["Gary",18,14,14,8,15,12,8]})
weapons ={"ShortSword":["Shortsword",1,6]}

player= units.Creature(creature["Gary"])
player.GetHP(8)
player.GetWeapon(weapons["ShortSword"])
eList.addEntity(player)

hpBox = InfoBox("HP:", 138,10,64,32)
hpBox.text.text = str(player.HP)

moveBox = InfoBox("M:", 266,10,32,32)
attackBox = InfoBox("A:", 330,10,32,32)
moveBox.text.text = "0"
attackBox.text.text = "0"

player.SetInitiative()
enemy = SpawnCreature("Goblin","ShortSword")
eList.addEntity(enemy)

maxInit = eList.maxInit()
initiative = maxInit
initBox = InfoBox("Init:",10,10,64,32)
initBox.text.text=str(initiative)

logBox = regs.TextObject(10, SCREENHEIGHT-106, (SCREENWIDTH-20), 32)
turnText = regs.TextObject(10,SCREENHEIGHT-74,(SCREENWIDTH-20), 32, text ="It is your turn")
helpBox =regs.TextObject(10,SCREENHEIGHT-42, (SCREENWIDTH-20),32, text ="Use arrow keys to move and attack, then ENTER to end turn")
boxes = [hpBox, initBox, logBox, helpBox, moveBox, attackBox]
print(player.init)
#boolean to create run-loop
running = True
playerTurn = False
enemy.Turn = False
count = 0
print ("gary strmod = ",player.strMod, " AC = ",player.AC)
print("goblin strmod = ",enemy.strMod, "AC = ", enemy.AC)
while running:
	if initiative == player.init and not playerTurn:
		playerTurn = True
		moveCount = 0
		attackCount = 0
	if playerTurn:
		moved = False

		moveBox.text.text = str(player.speed-moveCount)
		attackBox.text.text =str(1-attackCount)

		if moveCount < player.speed: moveOK = True
		else: moveOK = False
		#event handler
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				playerTurn = False
			elif event.type == KEYDOWN:
				if event.key == K_UP and moveOK:
					movePos = [0,-1]
					moved = True
				elif event.key == K_DOWN and moveOK:
					movePos = [0,1]
					moved = True
				elif event.key == K_LEFT and moveOK:
					movePos =[-1,0]
					moved = True
				elif event.key == K_RIGHT and moveOK:
					movePos =[1,0]
					moved = True
				elif event.key == K_RETURN:
					playerTurn = False

				if moved == True:
					targetPos = function.addPos(player.pos,movePos)
					check = eList.checkPos(targetPos)
					if check == None:
						player.Move(movePos)
						moveCount += 1
						print("Moved", moveCount, " spaces.")
					if type(check) == units.Creature and attackCount < 1:
						logBox.text = str(function.Attack(player, check)[2])
						attackCount += 1

	if not enemy.alive:
		print("You killed ", enemy.name,"!")
		eList.list.remove(enemy)
		count += 1
		enemy = SpawnCreature("Goblin","ShortSword")
		eList.addEntity(enemy)
		enemy.Turn = False


	if initiative == enemy.init and not playerTurn and not enemy.Turn:
		enemy.Turn = True
		enemy.moveCount = 0
		enemy.attackCount = 0
		enemy.inactive = 0

	if enemy.Turn:
		basicAI(enemy)
		pygame.time.wait(150)
		if not player.alive:
			print("You lost. You killed ", count, " enemies.")
			running = False

	#fill background white
	screen.fill((255,255,255))

	#draw all objects
	eList.draw(gameView)
	screen.blit(gameView,(10,42))
	for box in boxes:
		box.draw(screen)
	if playerTurn:
		turnText.draw(screen)
	#flip the display (updates)
	pygame.display.flip()
	if not (playerTurn or enemy.Turn):
		initiative = (initiative-1)%(maxInit+1)
		if initiative == 0: maxInit = eList.maxInit()
		initBox.text.text = str(initiative)
		print (initiative)
		pygame.time.wait(300)
	clock.tick(30)

pygame.quit()
