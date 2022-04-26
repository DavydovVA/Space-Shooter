from pygame import image, font


class Settings():

	def __init__(self):
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0, 0, 0)

		# Perks
		self.energy_increasing_flag = False
		self.energy_frames_counter = 0
		self.start_energy = 50
		self.energy = self.start_energy# %, if > 100, then more bullets
		self.energy_per_perk = 50
		self.bullet_speed = 1.2
		self.perk_speed = 0.6

		self.explode_duration = 500 # 500 frames

		# Ship settings
		self.ship_speed_x = 1.5
		self.ship_speed_y = 2

		self.driftShip_speed_x = 0.1
		self.driftShip_speed_y = 0.1

		self.start_ships_left = 10
		self.ships_left = self.start_ships_left

		# Space objects
		self.space_object_speed = [0.3, 0.5, 0.7, 0.9, 1.1]
		self.max_obj = 12
		self.total_obj = 0

		# Hud font
		self.hudFont = font.SysFont("serif", 48)
		self.hudColor = (180, 255, 0)
		self.hudCoords = (self.screen_width / 2 - 220, 0)
		self.goColor  = (180, 0, 0)# GameOver

		# Menu appearance
		self.menuFont = font.SysFont("serif", 48)
		self.menuActiveEl = (254, 254, 40)
		self.menuPassiveEl = (180, 0, 0)

		# Game session settigns
		self.game_active = True
		self.menu_active = True

		self.speed_up_coeff = 1.2

	def refreshStats(self):
		self.energy = 50
		self.total_obj = 0
		self.ships_left = 1
		self.game_active = True

		self.bullet_speed = 1.2
		self.perk_speed = 0.6
		self.space_object_speed = [0.3, 0.5, 0.7, 0.9]

		self.ships_left = self.start_ships_left
		self.energy = self.start_energy
