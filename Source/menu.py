from pygame import image, font
import pygame as pg


class Menu:

	def __init__(self, settings):
		self.startText = "Start Game"
		self.settingsText = "Settings"
		self.exitText = "Exit"

		self.maxObjectsText = "Max. Objects:"
		self.startLifeText = "Start Life:"
		self.startEnergyText = "Start Energy:"
		self.goBackText = "Go Back"

		self.settings = settings

		self.position = [[0, 1, 2], [0, 1, 2, 3]]
		self.activePos = 0

		self.activeScreen = 0 # 0 = menu, 1 = settings

	def drawMenu(self, screen):
		if self.activeScreen == 0:
			self.drawMainMenu(screen)
		elif self.activeScreen == 1:
			self.drawSettingsMenu(screen)

	def drawMainMenu(self, screen):
		startText = self.settings.menuFont.render(f"{self.startText}", True, self.chooseColor(0))
		settingsText = self.settings.menuFont.render(f"{self.settingsText}", True, self.chooseColor(1))
		exitText = self.settings.menuFont.render(f"{self.exitText}", True, self.chooseColor(2))

		screen.blit(startText, (self.settings.screen_width / 2 - 180, self.settings.screen_height / 2 - 150))
		screen.blit(settingsText, (self.settings.screen_width / 2 - 140, self.settings.screen_height / 2 - 60))
		screen.blit(exitText, (self.settings.screen_width / 2 - 100, self.settings.screen_height / 2 + 30))

	def drawSettingsMenu(self, screen):
		maxObjectsText = self.settings.menuFont.render(f"{self.maxObjectsText} {self.settings.max_obj}", True, self.chooseColor(0))
		startLifeText = self.settings.menuFont.render(f"{self.startLifeText} {self.settings.start_ships_left}", True, self.chooseColor(1))
		startEnergyText = self.settings.menuFont.render(f"{self.startEnergyText} {self.settings.start_energy}", True, self.chooseColor(2))
		goBackText = self.settings.menuFont.render(f"{self.goBackText}", True, self.chooseColor(3))

		screen.blit(maxObjectsText, (self.settings.screen_width / 2 - 200, self.settings.screen_height / 2 - 120))
		screen.blit(startLifeText, (self.settings.screen_width / 2 - 200, self.settings.screen_height / 2 - 50))
		screen.blit(startEnergyText, (self.settings.screen_width / 2 - 200, self.settings.screen_height / 2 + 20))
		screen.blit(goBackText, (self.settings.screen_width / 2 - 120, self.settings.screen_height / 2 + 90))

	def chooseColor(self, pos):
		if pos == self.activePos:
			return self.settings.menuActiveEl
		else:
			return self.settings.menuPassiveEl

	def nextMenuEl(self):
		if self.activePos != self.position[self.activeScreen][-1]:
			self.activePos += 1
		else:
			self.activePos = 0

	def previousMenuEl(self):
		if self.activePos != self.position[self.activeScreen][0]:
			self.activePos -= 1
		else:
			self.activePos = self.position[self.activeScreen][-1]

	def processAction(self): # TODO rename
		"""Process Enter key"""
		if self.activeScreen == 0:
			if self.activePos == self.position[0][0]:
				return 29 # start game
			if self.activePos == self.position[0][1]:
				self.activePos = 0
				self.activeScreen = 1
				return 0 # start game
			if self.activePos == self.position[0][2]:
				return -999
		elif self.activeScreen == 1:
			if self.activePos == self.position[1][3]:
				self.activePos = 0
				self.activeScreen = 0
				return 0

	def processLeftAction(self):
		if self.activePos == self.position[1][0]:
			if self.settings.max_obj > 1: self.settings.max_obj -= 1
		if self.activePos == self.position[1][1]:
			if self.settings.start_ships_left > 1: self.settings.start_ships_left -= 1
		if self.activePos == self.position[1][2]:
			if self.settings.start_energy > 0: self.settings.start_energy -= self.settings.energy_per_perk

		self.settings.refreshStats()

	def processRightAction(self):
		if self.activePos == self.position[1][0]:
			if self.settings.max_obj < 40: self.settings.max_obj += 1
		if self.activePos == self.position[1][1]:
			if self.settings.start_ships_left < 20: self.settings.start_ships_left += 1
		if self.activePos == self.position[1][2]:
			if self.settings.start_energy < 10000: self.settings.start_energy += self.settings.energy_per_perk

		self.settings.refreshStats()