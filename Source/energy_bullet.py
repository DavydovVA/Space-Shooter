import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
	image = pg.image.load("images/bullet.bmp")

	def __init__(self, settings, ship):
		super().__init__()

		self.settings = settings
		self.rect = Bullet.image.get_rect()

		self.rect.x = ship.rect.centerx + 5
		self.rect.y = ship.rect.centery - 5

		self.center = [float(self.rect.x), float(self.rect.y)]

	def update(self):
		self.center[0] += self.settings.bullet_speed

		self.rect.x = self.center[0]