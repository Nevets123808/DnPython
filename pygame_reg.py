import pygame
pygame.init()
screen = pygame.display.set_mode((640,400))
COLOUR_INERT =(30,30,30)
COLOUR_INACTIVE = pygame.Color('lightskyblue3')
COLOUR_ACTIVE = pygame.Color('dodgerblue2')
FONT =pygame.font.Font(None, 32)

class TextObject:
	def __init__ (self, x, y ,w, h, text = "", textColour = COLOUR_ACTIVE, boxColour = COLOUR_INERT):
		self.rect = pygame.Rect(x,y,w,h)
		self.colour = boxColour
		self.text = text
		self.textColour = textColour
		self.txt_surface = FONT.render(text, True, textColour)
	def handle_event(self, event):
		pass
	def update(self):
		width = max(200, self.txt_surface.get_width()+10)
		self.rect.w = width

	def draw(self, screen):
		self.txt_surface = FONT.render(self.text, True, self.textColour)
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		pygame.draw.rect(screen, self.colour, self.rect, 2)

class InputBox(TextObject):
	def __init__ (self, x, y ,h, w, text = "", activeColour= COLOUR_ACTIVE, inactiveColour=COLOUR_INACTIVE):
		super().__init__(x,y,h,w,text)
		self.activeColour = activeColour
		self.inactiveColour = inactiveColour
		self.colour = self.inactiveColour
		self.active = False

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.colour = self.activeColour if self.active else self.inactiveColour
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					print(self.text)
					self.text =""
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text+= event.unicode
				self.txt_surface = FONT.render(self.text, True, self.colour)

class Field:
	def __init__ (self, name, x,y,w,h):
		self.name = name
		self.label_width = len(name)*32
		self.input_width = w -self.label_width
		self.label = TextObject(x,y,self.label_width,h,self.name)
		self.input = InputBox(x+self.label_width,y,self.input_width,h)

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
	return Field(name,x,y,FIELD_WIDTH,FIELD_HEIGHT)

def main():
	clock = pygame.time.Clock()
	text_box = TextObject(50, 100,140, 16, "Hello:")
	input_box1 = InputBox(100,100,140,16)
	input_box2 = InputBox(100,300,140,16)
	boxes = [text_box, input_box1, input_box2]
	done =False

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			for box in boxes:
				box.handle_event(event)
		for box in boxes:
			box.update()

		screen.fill((30,30,30))
		for box in boxes:
			box.draw(screen)

		pygame.display.flip()
		clock.tick(30)

if __name__ == '__main__':
	main()
	pygame.quit()
