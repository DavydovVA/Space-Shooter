import pygame as pg
from pygame.sprite import Sprite

class SpaceObject(Sprite):
	
	def __init__(self, settings, screen, skin, position, speed_num):
		""""""
		super().__init__()
		self.settings = settings
		self.screen = screen
		self.skin = skin
		self.position = position #задает высоту появления объекта
		self.speed_num = speed_num
		
		if self.skin == 1:
			self.image = pg.image.load("images/earth(CUT).bmp")# TEST  before
		else:
			self.image = pg.image.load("images/moon(CUT).bmp")
			
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		self.rect.x = self.screen_rect.right
		#self.rect.x = self.screen_rect.left + 200 #TEMP!!!!!!!!!!!!!!!!
		self.rect.y = self.screen_rect.centery + (self.settings.screen_height / 9) * self.position
		
		self.center = [float(self.rect.x), float(self.rect.y)]
		
	
	def update(self):
		self.center[0] -= self.settings.space_object_speed[self.speed_num]
		
		self.rect.x = self.center[0]
		
	#def blitme(self):
	#	self.screen.blit(self.image, self.rect)
