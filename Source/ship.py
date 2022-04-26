import pygame as pg
from random import randint

class Ship():
	shipImage = pg.image.load("images/ship2.bmp")
	crShipImage = pg.transform.scale(pg.image.load("images/ship2crushed.bmp"), (80, 80))

	def __init__(self, settings, screen):
		self.screen = screen
		self.settings = settings

		self.image = Ship.shipImage
		#0, 0, 80, 80 (topX, topY, bottomX, bottomY)
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# Still alive if False
		self.crushed = False

		self.rect.centerx = self.screen_rect.left + 50
		self.rect.centery = self.screen_rect.centery

		self.center = [float(self.rect.centerx), float(self.rect.centery)]

		# Fields for returning to start position
		self.x_step = 0
		self.y_step = 0
		self.end_position = self.center.copy() # relative to the beginning of the movement
		self.start_movement_flag = False

		# Flags for continuous moving
		self.up = False
		self.down = False
		self.left = False
		self.right = False

		# Fields for Ship's Drifting (menu, GO)
		# up, right, down, left, first, fourth, third, second
		self.edges = [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5]
		self.drift_history = [-1 for i in range(0, len(self.edges) * 3)]
		self.drift_direction_counter = 0
		self.current_drift_direction = 0
		self.center_history = [[0, -1], [-1, 0], [0, 0]]
		self.drift_frames = 500

	def update(self):
		"""Update Ship's position while in game"""
		if self.crushed:
			return

		# Cheking borders, moving
		if self.up and self.rect.top > self.screen_rect.top:
			self.center[1] -= self.settings.ship_speed_y
		if self.down and self.rect.bottom < self.screen_rect.bottom:
			self.center[1] += self.settings.ship_speed_y
		self.rect.centery = self.center[1]

		# Checking borders, moving + slowing down while in specific zones
		if self.left and self.rect.right >= self.screen_rect.right / 3.5:
			self.center[0] -= ((self.screen_rect.right - self.rect.right) / (2 * self.screen_rect.right)) * self.settings.ship_speed_x
		elif self.left and self.rect.left > self.screen_rect.left:
			self.center[0] -= self.settings.ship_speed_x
		if self.right and self.rect.right < self.screen_rect.right / 3.5:
			self.center[0] += self.settings.ship_speed_x
		if self.right and self.rect.right >= self.screen_rect.right / 3.5 and self.rect.right < self.screen_rect.right:
			self.center[0] += ((self.screen_rect.right - self.rect.right) / (2 * self.screen_rect.right)) * self.settings.ship_speed_x
		self.rect.centerx = self.center[0]

	def cruShip(self):
		"""Give a crushed status for ship"""
		self.crushed = True
		self.image = Ship.crShipImage

	def restoreShip(self):
		self.crushed = False
		self.image = Ship.shipImage

	def addToDriftHistory(self, value):
		self.drift_history = [self.drift_history[-1]] + self.drift_history[:-1]

		self.drift_history[0] = value

	def addToCenterHistory(self, value):
		self.center_history = [self.center_history[-1]] + self.center_history[:-1]

		self.center_history[0] = value

	def checkCenterHistory(self):
		"""Check, if Ship is stuck near the screen border"""
		counter = 0
		for i in range (1, 3):
			if self.center_history[0] == self.center_history[i]:
				counter += 1

		if counter == 2:
			return 1

		return 0

	def getDriftDirection(self):
		"""Calculate a direction in which to drift"""
		edges_copy = [0 for i in range(0, len(self.edges))]
		additives = [0 for i in range(0, len(self.edges))]

		for i in range(0, len(self.edges)):
			edges_copy[i] = ((len(self.drift_history) - self.drift_history.count(i)) / len(self.drift_history)) * self.edges[i]

		for i in range(0, len(additives)):
			for j in range(0, len(edges_copy)):
				if j == i:
					continue
				additives[i] += (self.edges[j] - edges_copy[j]) / (len(self.edges) - 1)

		total = 0
		for i in range(0, len(additives)):
			self.edges[i] = edges_copy[i] + additives[i]
			total += self.edges[i]

		if total != 100:
			shortage = 100 - total
			destination = randint(0, 7)
			self.edges[destination] += shortage

		direction_value = randint(1, 100)

		value = 0;
		for i in range(0, len(self.edges)):
			value += self.edges[i]
			if direction_value <= value:
				return i

		return 3

	def driftShip(self):
		"""Change Ship's position in menu and after Game Over"""
		self.drift_direction_counter += 1
		if self.drift_direction_counter % self.drift_frames == 0 or self.checkCenterHistory() == 1: # % frames
			self.drift_direction_counter = 0
			self.drift_frames = randint(200, 700)

			direction = self.getDriftDirection()
			self.current_drift_direction = direction

			self.addToDriftHistory(direction)
			self.addToCenterHistory(self.center.copy())
		else:
			direction = self.current_drift_direction
			self.addToCenterHistory(self.center.copy())

		# Y
		if (direction == 0 or direction == 4 or direction == 7) and self.rect.top > self.screen_rect.top:
			self.center[1] -= self.settings.driftShip_speed_y
		if (direction == 2 or direction == 5 or direction == 6) and self.rect.bottom < self.screen_rect.bottom:
			self.center[1] += self.settings.driftShip_speed_y
		self.rect.centery = self.center[1]
		# X
		if (direction == 1 or direction == 4 or direction == 5) and self.rect.left > self.screen_rect.left:
			self.center[0] -= self.settings.driftShip_speed_x
		if (direction == 3 or direction == 6 or direction == 7) and self.rect.right < self.screen_rect.right:
			self.center[0] += self.settings.driftShip_speed_x
		self.rect.centerx = self.center[0]

	def moveToStartPos(self):
		"""Move Ship to a place near start position"""
		if abs(self.center[0] - self.end_position[0]) < 50 and abs(self.center[1] - self.end_position[1]) < 50:
			# On start position
			self.start_movement_flag = False
			return 0

		# Calculate movement step
		if self.start_movement_flag == False:
			self.start_movement_flag = True
			self.x_step = (abs(self.center[0] - self.end_position[0])) / 100
			self.y_step = (abs(self.center[1] - self.end_position[1])) / 100

		# X
		if self.center[0] < self.end_position[0]:
			self.center[0] += self.x_step
		elif self.center[0] > self.end_position[0]:
			self.center[0] -= self.x_step
		self.rect.centerx = self.center[0]
		# Y
		if self.center[1] < self.end_position[1]:
			self.center[1] += self.y_step
		elif self.center[1] > self.end_position[1]:
			self.center[1] -= self.y_step
		self.rect.centery = self.center[1]

		return 1

	def blitme(self):
		"""Draw ship"""
		self.screen.blit(self.image, self.rect)
