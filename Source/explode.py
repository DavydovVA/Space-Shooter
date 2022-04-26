import pygame as pg
from pygame.sprite import Sprite


class Explode(Sprite):
	explodeImage = pg.transform.scale(pg.image.load("images/explode1.bmp"), (80, 80)) # param

	def __init__(self, settings, position):
		super().__init__()

		self.image = Explode.explodeImage
		self.settings = settings
		self.rect = position
		self.position = position.copy()

		self.duration = self.settings.explode_duration

	def update(self):
		self.duration -= 1

		value = self.duration / self.settings.explode_duration
		if value > 0:
			self.image = pg.transform.scale(Explode.explodeImage, (int(80 * value), int(80 * value))) # param

		self.rect[0] = self.position[0] + 80 * (1 - value) / 2 # param
		self.rect[1] = self.position[1] + 80 * (1 - value) / 2 # param