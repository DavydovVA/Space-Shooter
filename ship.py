import pygame as pg

class Ship():
	
	def __init__(self, settings, screen):
		self.screen = screen
		self.settings = settings
		
		#Загрузка изображения и получение размеров изображение и экрана
		self.image = pg.image.load("images/ship2.bmp") #TEST before
		self.rect = self.image.get_rect() #0, 0, 80, 80		первые два - местополжение left top части
		self.screen_rect = screen.get_rect()
		
		#это координаты прорисовки центра изображения, не та часть self.rect, на 
		#соотвественную половину размера изоюражения больше left top
		#можно записать self.rect.center = ..., ...
		self.rect.centerx = self.screen_rect.left + 50
		self.rect.centery = self.screen_rect.centery
		
		self.center = [float(self.rect.centerx), float(self.rect.centery)]
		
		#Флаги для непрерывного движения
		self.up = False
		self.down = False
		self.left = False
		self.right = False
		
		
	def update(self):
		#Границы плюс описание движения
		if self.up and self.rect.top > self.screen_rect.top:
			self.center[1] -= self.settings.ship_speed_y
		if self.down and self.rect.bottom < self.screen_rect.bottom:
			self.center[1] += self.settings.ship_speed_y
		self.rect.centery = self.center[1]
		
		if self.left and self.rect.left > self.screen_rect.left:
			self.center[0] -= self.settings.ship_speed_x
		if self.right and self.rect.right < (self.screen_rect.right)/3:
			self.center[0] += self.settings.ship_speed_x
		self.rect.centerx = self.center[0]
		
		
	def blitme(self):
		"""рисует корабль в текущей позиции"""
		self.screen.blit(self.image, self.rect)
