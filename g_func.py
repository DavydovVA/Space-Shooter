import sys
import pygame as pg
from random import randint, seed
from space_object import SpaceObject
from perk import Perk

def check_keydown_events(event, ship):
	if event.key == pg.K_UP:
		ship.up = True
	if event.key == pg.K_DOWN:
		ship.down = True
	if event.key == pg.K_LEFT:
		ship.left = True
	if event.key == pg.K_RIGHT:
		ship.right = True
	if event.key == pg.K_q:
		sys.exit()
		
def check_keyup_events(event, ship):
	if event.key == pg.K_UP:
		ship.up = False
	if event.key == pg.K_DOWN:
		ship.down = False
	if event.key == pg.K_LEFT:
		ship.left = False
	if event.key == pg.K_RIGHT:
		ship.right = False
	
	
def check_events(ship):
	"""Обработка нажатий клавиш"""
	for event in pg.event.get():
		if event.type == pg.QUIT:
			sys.exit()
		if event.type == pg.KEYDOWN:
			check_keydown_events(event, ship)
		if event.type == pg.KEYUP:
			check_keyup_events(event, ship)


def update_screen(g_settings, screen, ship, objects, perk):
	"""Прорисовка экрана"""
	#screen.fill(g_settings.bg_color)
	ship.blitme()
	objects.draw(screen)
	perk.draw(screen)
	#Отоюражение последнего прорисованного экрана
	
	
	pg.display.flip()
	
	
def check_obj_edges(settings, screen, objects):
	"""Граница вне экрана и удаление"""
	screen_rect = screen.get_rect()
	for obj in objects.copy():
		if obj.rect.right < screen_rect.left:
			objects.remove(obj)
			settings.total_obj -= 1
			

def check_radius(ship_point_coord, obj_center_coord, wing):
	#Пока радиус задаем перманентно но неявно(в формуле)
	#Ships body
	first_catet = abs(ship_point_coord[0] - obj_center_coord[0])
	second_catet = abs(ship_point_coord[1] - obj_center_coord[1])
	gipotinuza_body = (first_catet**2 + second_catet**2)**(0.5)
	
	#Ships wing
	first_wing_catet = abs(wing[0] - obj_center_coord[0])
	second_wing_catet = abs(wing[1] - obj_center_coord[1])
	gipotinuza_wing = (first_wing_catet**2 + second_wing_catet**2)**(0.5)
	
	#print("GIP: " + str(gipotinuza))
	if (gipotinuza_body - 38) < 0 or (gipotinuza_wing - 38) < 0:
		return True
	else:
		return False
	
	
def get_point(ship, up, right):
	"""Получение одной из точчек углов"""
	#Размер каждого изоюражения пока что 80 на 80
	point = [0, 0]
	
	if up and right: # 1st
		point[0] = ship.rect.x + 40
		point[1] = ship.rect.y + 10
	if up and not right: # 2nd
		point[0] = ship.rect.x - 40
		point[1] = ship.rect.y + 20
	if not up and not right: # 3rd
		point[0] = ship.rect.x - 40
		point[1] = ship.rect.y - 20
	if not up and right: #4th
		point[0] = ship.rect.x + 40
		point[1] = ship.rect.y - 10
	
	return point
	
def crit_hit(settings, screen, obj, ship):
	#Сверху снизу слева справа    либо точки либо стороны
	up, right= False, False

	if obj.rect.y > ship.rect.y:#сверху
		up = True
	else:#снизу
		up = False
	if obj.rect.x > ship.rect.x:#Справа
		right = True
	else:#Слева
		right = False
	
	#print("UP: " + str(up))
	#print("RIGHT: " + str(right))
	#получить координаты нуэной точки корабля и проверить расстояние до центра
	ship_point_coord = get_point(ship, up, right)
	obj_center_coord = [obj.rect.x, obj.rect.y]
	#Вычисление расстояния от полученной точки до центра obj
	
	#print("SHIP: " + str(ship_point_coord))
	#print("OBJ: " + str(obj_center_coord))
	
	#координаты концов крыльев
	wing = [0, 0]
	if up == True:
		wing = top_wing = [ship.rect.x -15, ship.rect.y + 40]
	else:
		wing = bottom_wing = [ship.rect.x - 15, ship.rect.y - 40]

	
	return check_radius(ship_point_coord, obj_center_coord, wing)	
	
def check_perk_edges(screen, perks):
	"""Граница вне экрана и удаление"""
	screen_rect = screen.get_rect()
	for perk in perks.copy():
		if perk.rect.right < screen_rect.left:
			perks.remove(perk)

def perk_hit(settings, perk):
	if perk.perk_type == 1:
		settings.ships_left += 1
	else:
		settings.bullet += 1
	
def update_objects(settings, screen, objects, ship, perk):
	"""Меняет координаты и удаляет лишние объекты а так же коллизия с кораблем"""
	objects.update()
	perk.update()
	check_obj_edges(settings, screen, objects)
	check_perk_edges(screen, perk)
	
	#Проверка коллизии с кораблем
	for obj in objects.copy():
		if pg.sprite.collide_rect(ship, obj):
			if crit_hit(settings, screen, obj, ship):
				objects.remove(obj)
				settings.ships_left -= 1
				settings.total_obj -= 1
				#wait = input()
				print("!")
				
	for prk in perk.copy():
		if pg.sprite.collide_rect(ship, prk):
			perk_hit(settings, prk)
			perk.remove(prk)
			
			
	if settings.ships_left < 1:
		settings.game_active = False
		print("Game Over")
		#print(settings.ships_left)

def create_object(settings, screen, objects):
	"""Создает новый объект по некоторым условиям"""
	flag = True
	for obj in objects.copy():
		if not obj.rect.x < settings.screen_width - int(1.2*80):
			flag = False
	if flag:
		seed(version=2)
		skin = randint(1,2)
		position = randint(-4, 3)
		speed_num = randint(-1, 2)
		obj = SpaceObject(settings, screen, skin, position, speed_num)
		
		settings.total_obj += 1
		
		objects.add(obj)
	
def create_perk(settings, screen, perk):
	seed(version=2)
	value = randint(0, 1000)
	if value == 200:
		skin = randint(0, 2)
		position = randint(-8, 7)
		
		new_perk = Perk(settings, screen, skin, position)
		perk.add(new_perk)
		
		
def add_obj_group(settings, screen, objects, perk):
	"""Добавляет космический объект к группе"""
	create_object(settings, screen, objects)
	create_perk(settings, screen, perk)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
