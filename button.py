import pygame
import sys

# pygame.init()
# screen = pygame.display.set_mode((800, 800))
# pygame.display.set_caption("Button!")

class Button():
	# def __init__(self, screen, image=None, x_pos=0, y_pos=0, text_input=""):
	def __init__(self, screen, color, x_pos=0, y_pos=0, text_input=""):
		# self.image = image
		self.screen = screen
		self.color = color
		self
		self.x_pos = x_pos
		self.y_pos = y_pos
		# self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.rect = pygame.draw.rect(self.screen, pygame.Color(self.color), (self.x_pos+18, self.y_pos, 60, 30))
		self.text_input = text_input
		self.main_font = pygame.font.SysFont("cambria", 14)
		self.text = self.main_font.render(self.text_input, True, "black")
		self.text_rect = self.text.get_rect(center=(self.x_pos+45, self.y_pos+16))

	def update(self):
		# self.screen.blit(self.image, self.rect)__
		self.screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			print("Button Press!")
			return True

	def toggleColor(self):
		if self.color == 'green':
			self.color = 'gray'
		else:
			self.color = 'green'
		self.rect = pygame.draw.rect(self.screen, pygame.Color(self.color), (self.x_pos+18, self.y_pos, 60, 30))
		self.text = self.main_font.render(self.text_input, True, "black")
		self.text_rect = self.text.get_rect(center=(self.x_pos+45, self.y_pos+16))

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = main_font.render(self.text_input, True, "green")
		else:
			self.text = main_font.render(self.text_input, True, "gray")

# button_surface = pygame.image.load("button.png")
# button_surface = pygame.transform.scale(button_surface, (400, 150))

# button = Button(button_surface, 400, 300, "Button")

# while True:
	# for event in pygame.event.get():
		# if event.type == pygame.QUIT:
			# pygame.quit()
			# sys.exit()
		# if event.type == pygame.MOUSEBUTTONDOWN:
			# button.checkForInput(pygame.mouse.get_pos())

	# screen.fill("white")

	# button.update()
	# button.changeColor(pygame.mouse.get_pos())

	# pygame.display.update()