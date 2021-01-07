import units
import function
import pygame
import pygame_reg as regs
import ast
import csv

class Field:
	def __init__ (self, name, x,y,w,h):
		self.name = name
		self.label_width = len(name)*32
		self.input_width = w -self.label_width
		self.label = regs.TextObject(x,y,self.label_width,h,self.name)
		self.input = regs.InputBox(x+self.label_width,y,self.input_width,h)

	def handle_event(self,event):
		self.label.handle_event(event)
		self.input.handle_event(event)

	def update(self):
		self.label.update()
		self.input.update()

	def draw(self,screen):
		self.label.draw(screen)
		self.input.draw(screen)

def New_Field (name, x, y):
	return regs.Field(name,x,y,FIELD_WIDTH,FIELD_HEIGHT)

def PopulateDictionary(boxes):
	dict={}
	statArray = []
	for field in boxes:
		if field.name == "Name:":
			statArray.append(field.input.text)
		else:
			statArray.append(int(field.input.text))
	dict.update({boxes[0].input.text:statArray})
	return dict

def LoadFile():
	with open("creatures.dat","r") as file:
		dict = ast.literal_eval(file.read())
	return dict

def WriteFile(dict):
	with open("creatures.dat","wt") as file:
		file.write(str(dict))

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT =640

FIELD_WIDTH = 200
FIELD_HEIGHT = 32

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def main():
	creatures = LoadFile()
	print (creatures)
	clock = pygame.time.Clock()
	nameField = New_Field("Name:",10,10)
	strField = New_Field("STR:", 10, 50)
	dexField = New_Field("DEX:", 10, 100)
	conField = New_Field("CON:", 10, 150)
	intField = New_Field("INT:", 10, 200)
	wisField = New_Field("WIS:", 10, 250)
	chaField = New_Field("CHA:", 10, 300)
	hpField = New_Field("HP:", 260, 50)
	boxes = [nameField,strField,dexField, conField, intField, wisField, chaField, hpField]

	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			for box in boxes:
				box.handle_event(event)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_HOME:
					creature = PopulateDictionary(boxes)
					print (creature)
					creatures.update(creature)
				if event.key == pygame.K_END:
					print (creatures)
					WriteFile(creatures)

		for box in boxes: box.update()

		screen.fill((30,30,30))

		for box in boxes: box.draw(screen)

		pygame.display.flip()
		clock.tick(30)

if __name__ == "__main__":
	main()
	pygame.quit()

