from pygame import image
class Settings():
	
	def __init__(self):
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0, 0, 0)
		
		self.perk_speed = 1
		#То что может увеличиваться перками
		self.bullet = 0
		#Настройи корабля
		self.ship_speed_x = 1.5
		self.ship_speed_y = 2
		self.ships_left = 5

		#настройки космических объектов
		self.space_object_speed = [1.5, 2, 2.5]
		self.max_obj = 12 #Пока лишнее
		self.total_obj = 0
			
		#настройки активности игры
		self.game_active = True

		
