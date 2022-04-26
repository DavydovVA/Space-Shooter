import pygame as pg

from settings import Settings 
import g_func as gf
from ship import Ship
from perk import Perk
from space_object import SpaceObject
from explode import Explode
from pygame.sprite import Group

from menu import Menu


def speedUpObjs(settings):
	coeff = settings.speed_up_coeff
	settings.perk_speed = settings.perk_speed * coeff
	for speed_num in range(0, len(settings.space_object_speed)):
		settings.space_object_speed[speed_num] = settings.space_object_speed[speed_num] * coeff
	settings.bullet_speed = settings.bullet_speed * coeff


def runGameSession(settings, screen, ship):
	objects = Group()
	perks = Group()
	bullets = Group()
	explodes = Group()

	bgImage = pg.image.load("images/bg.bmp").convert() #Чтобы быстрее прорисовывался bg

	settings.menu_active = False

	restart_counter = 0 # == 1, speed up objects, == 2, skip speeding up
	speed_up_frame_counter = -1
	while True:
		if gf.processKeyBoard(settings, ship, bullets, 0) == 28:
			restart_counter += 1

		if restart_counter != 0: # if pressed Y, restart initiated
			while True: # == do while false
				if restart_counter == 1:
					speed_up_frame_counter += 1
					if speed_up_frame_counter % 10 == 0:
						speedUpObjs(settings) # all speeds in settings

				if not (len(objects) == 0 and len(perks) == 0 and len(bullets) == 0) and restart_counter < 2:
					break

				settings.menu_active = True
				screen.blit(bgImage, [0, 0])
				gf.updateScreen(settings, screen, ship, objects, perks, bullets, explodes)

				return 28 # Random Code

		if settings.game_active:
			ship.update()
			
			# Spawn objects
			if settings.total_obj < settings.max_obj:  
				gf.spawnObjects(settings, screen, objects, perks)

			# Move objects
			if gf.updateObjects(settings, screen, objects, ship, perks, bullets, explodes) == -999:
				settings.game_active = False

		else:# TODO get rid of this shit
			gf.updateObjects(settings, screen, objects, ship, perks, bullets, explodes)
			ship.driftShip()

		# Draw background image
		screen.blit(bgImage, [0, 0])

		# Draw objects
		gf.updateScreen(settings, screen, ship, objects, perks, bullets, explodes)


def runGame():
	pg.init()
	pg.font.init()
	settings = Settings()

	screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
	pg.display.set_caption("Spice shooter")
	bgImage = pg.image.load("images/bg.bmp").convert() #Чтобы быстрее прорисовывался bg

	screen.blit(bgImage, [0, 0])
	menu = Menu(settings)
	ship = Ship(settings, screen)

	fly_to_start_flag = 0 # 0, 1, 2 status
	while True:
		screen.blit(bgImage, [0, 0])
		menu.drawMenu(screen)

		if fly_to_start_flag == 1:
			if ship.moveToStartPos() == 1:
				gf.updateScreen(settings, screen, ship, 0, 0, 0, 0)#
				continue
		else:
			fly_to_start_flag = 0

		if fly_to_start_flag != 1:
			code = gf.processKeyBoard(settings, 0, 0, menu)

		if code == 29:
			ship.restoreShip()

			if fly_to_start_flag == 0:
				fly_to_start_flag = 1
				continue
			else:
				fly_to_start_flag = 2

			if runGameSession(settings, screen, ship) != 28:
				break
			else:
				fly_to_start_flag = 0
				settings.refreshStats()
		elif code == -999:
			break
		else:
			ship.driftShip()
			gf.updateScreen(settings, screen, ship, 0, 0, 0, 0)

	pg.quit()


if __name__ == '__main__':
	runGame()
	
#5) Ускорение поанет вместе с зарядкой энерги на пулю
#8) Скины космических объектов и выбор скина корабля в настройках (Death Star)
#9) Заряд энергии для пули зажатием Space, E - энергия для ускорения при нажатии клавиши + деактивация(в поле замедления, эергия тратится)
#7) Игровые события (f.e.: Затишье перед жепой + warning before)
#6) Игровой счет (за avoid объектов на близком расстянии + уничтожение пулей)
#n) Обломки корабля ?????