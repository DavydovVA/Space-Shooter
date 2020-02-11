import pygame as pg
from pygame.sprite import Sprite

#Так же рандомно перки спавнить

class Perk(Sprite):
	
	def __init__(self, settings, screen, perk_type, position):
		super().__init__()
		self.settings = settings
		self.screen = screen
		self.perk_type = perk_type
		self.position = position
		
		if self.perk_type == 1:
			self.image = pg.image.load("images/perk_+1life.bmp")
		else:
			self.image = pg.image.load("images/perk_energy_bullet.bmp")
		
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		self.rect.x = self.screen_rect.right
		#self.rect.x = self.screen_rect.left + 200 #TEMP!!!!!!!!!!!!!!!!
		self.rect.y = self.screen_rect.centery + (self.settings.screen_height / 20) * self.position
		
		self.center = [float(self.rect.x), float(self.rect.y)]

	def update(self):
		self.center[0] -= self.settings.perk_speed
		
		self.rect.x = self.center[0]
		
	#def blitme(self):
	#	self.screen.blit(self.image, self.rect)
