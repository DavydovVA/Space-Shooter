import pygame as pg

from settings import Settings 
import g_func as gf
from ship import Ship
from perk import Perk
from space_object import SpaceObject #чекнуть че будет если убарть
from pygame.sprite import Group


def run_game():
	#Game nitialization and creating screen
	pg.init()
	g_s = Settings()
	screen = pg.display.set_mode((g_s.screen_width, g_s.screen_height))
	pg.display.set_caption("Alpha ver.")
	
	#создание игровых объектов
	ship = Ship(g_s, screen)
	objects = Group()###############################3
	
	clock = pg.time.Clock() # convert без этого не пашет
	#gf.add_obj_group(g_s, screen, objects)#TEMP
	
	bg_image = pg.image.load("images/bg.bmp").convert() #Чтою быстрее прорисовывался bg
	
	perk = Group()
	temp = -1
	while True:
		gf.check_events(ship)#обработка клавиш
		
		if g_s.game_active:
			ship.update()
			
			if g_s.total_obj < g_s.max_obj:  
				gf.add_obj_group(g_s, screen, objects, perk)
			
			
			if not g_s.bullet == temp:
				print(g_s.bullet)
			temp = g_s.bullet
			
			#print('')#Чисто чекать HIT'ы
			
			gf.update_objects(g_s, screen, objects, ship, perk)
		
		screen.blit(bg_image, [0, 0])	
		gf.update_screen(g_s, screen, ship, objects, perk)
		#clock.tick(300) #???????
		
	
#///////////////////////////////////////////////////////////////////////

run_game()


#ОБУЧИТЬ НЕЙРОСЕТЬ УПРАВЛЕНИЮ КОРАБЛЕМ!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#Перка стрельба энергетической пулей
#Настроить спавн объектов
#траектория космических объектов (не перков)
"""END"""
#Menu
#Счёт игровой
#Сохранения игровой статистики и рекорды
#Посмотреть на плавность изоюражения
#Рандом по закону для скорости движения (большая скорость очень редкая)


















