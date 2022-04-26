import pygame as pg
from pygame.sprite import Sprite
from math import sin


class SpaceObject(Sprite):
	earthImage = pg.image.load("images/earth(CUT).bmp")
	moonImage = pg.image.load("images/moon(CUT).bmp")

	def __init__(self, settings, screen, skin, position, speed_num, traectory_num, amplitude, frequency):
		super().__init__()

		self.settings = settings
		self.screen = screen
		self.skin = skin
		self.position = position #задает высоту появления объекта
		self.speed_num = speed_num
		self.traectory_num = traectory_num # тип траектории (минус, и тд)

		self.amplitude = amplitude
		self.frequency = frequency

		if self.skin == 1:
			self.image = SpaceObject.earthImage
		else:
			self.image = SpaceObject.moonImage

		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()

		self.rect.x = self.screen_rect.right
		self.starty = self.screen_rect.centery + (self.settings.screen_height / 9) * self.position
		self.rect.y = self.starty

		self.center = [float(self.rect.x), float(self.rect.y)]

	def update(self):
		self.center[0] -= self.settings.space_object_speed[self.speed_num]

		self.rect.x = self.center[0]

		if self.traectory_num == 1:
			self.rect.y = self.amplitude * sin(self.rect.x * self.frequency) + self.starty
