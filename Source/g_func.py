import sys
import pygame as pg
from random import randint, seed
from space_object import SpaceObject
from perk import Perk
from energy_bullet import Bullet
from explode import Explode
from menu import Menu


###########################
### KB processing block ###
###########################

def processKeyDowns(event, settings, ship, bullets, menu):
	if event.key == pg.K_UP:
		if not menu:
			ship.up = True
		else:
			menu.previousMenuEl()
	if event.key == pg.K_DOWN:
		if not menu: 
			ship.down = True
		else:
			menu.nextMenuEl()
	if event.key == pg.K_LEFT:
		if not menu: ship.left = True
		else: menu.processLeftAction()
	if event.key == pg.K_RIGHT:
		if not menu: ship.right = True
		else: menu.processRightAction()
	if event.key == pg.K_q:
		if not menu: sys.exit()
	if event.key == pg.K_y and settings.game_active == False:
		return 28 #28 = start new game
	if event.key == pg.K_KP_ENTER and menu:
		return menu.processAction()

	if menu: # TEMP ???
		return 0
	# For smoother handling (may be TEMP)
	if not settings.energy < 100:
		if event.key == pg.K_SPACE:
			createBullet(settings, ship, bullets)
	else:
		if event.key == pg.K_SPACE:
			settings.energy_increasing_flag = True
	
	return 0


def processKeyUps(event, ship, settings):
	if event.key == pg.K_UP:
		ship.up = False
	if event.key == pg.K_DOWN:
		ship.down = False
	if event.key == pg.K_LEFT:
		ship.left = False
	if event.key == pg.K_RIGHT:
		ship.right = False
	if event.key == pg.K_SPACE:
		settings.energy_increasing_flag = False


def processKeyBoard(settings, ship, bullets, menu):
	"""Keyboard events processing"""
	for event in pg.event.get():
		if event.type == pg.QUIT:
			sys.exit()
		if event.type == pg.KEYDOWN:
			return processKeyDowns(event, settings, ship, bullets, menu)
		if event.type == pg.KEYUP and not menu: # TEMP
			processKeyUps(event, ship, settings)
			
	return 0


######################
### Updating block ###
######################

def updateScreen(settings, screen, ship, spaceObjs, perks, bullets, explodes):
	"""Screen drawing"""
	if settings.game_active == True and settings.menu_active == False:
		hudText = settings.hudFont.render(f"Life:{settings.ships_left} Energy:{settings.energy}%", True, settings.hudColor)
		screen.blit(hudText , settings.hudCoords)

	if spaceObjs != 0:
		spaceObjs.draw(screen)
		perks.draw(screen)
		bullets.draw(screen)

	if settings.game_active == False and settings.menu_active == False:
		gameOverText = settings.hudFont.render("GAME OVER", True, settings.goColor)
		screen.blit(gameOverText, (settings.screen_width / 2 - 160, settings.screen_height / 2 - 60))

	ship.blitme()
    
	if explodes != 0:
		explodes.draw(screen)

	pg.display.flip()


def updateObjects(settings, screen, spaceObjs, ship, perk, bullets, explodes):
	"""Меняет координаты и удаляет лишние объекты а так же коллизия с кораблем"""
	spaceObjs.update()
	perk.update()
	bullets.update()
	explodes.update()

	checkSpaceObjsEdges(settings, screen, spaceObjs)
	checkPerkEdges(screen, perk)
	checkBulletEdges(screen, bullets)

	if settings.energy_increasing_flag:
		increaseEnergyBulletCharge(settings)
	
	if settings.game_active == False:
		return 1

	# Check explosion duration
	for explode in explodes:
		if explode.duration <= 0:
			explodes.remove(explode)

	#Проверка коллизии с кораблем
	for obj in spaceObjs:#.copy():
		if pg.sprite.collide_rect(ship, obj):
			if spaceObjectHit(settings, screen, obj, ship):
				spaceObjs.remove(obj)

				explode = Explode(settings, obj.center)
				explodes.add(explode)

				if settings.game_active == True:
					settings.ships_left -= 1
				settings.total_obj -= 1

				if settings.ships_left < 1:
					explode = Explode(settings, ship.rect.copy())
					explodes.add(explode)
					ship.cruShip()

	for prk in perk:
		if pg.sprite.collide_rect(ship, prk):
			perkHit(settings, prk)
			perk.remove(prk)

	for bullet in bullets:
		for obj in spaceObjs:
			if pg.sprite.collide_rect(bullet, obj):
				if not bulletHit(settings, screen, obj, bullet):
					continue

				explode = Explode(settings, obj.center)
				explodes.add(explode)

				spaceObjs.remove(obj)
				bullets.remove(bullet)
				settings.total_obj -= 1

	if settings.ships_left < 1:
		settings.game_active = False
		return -999 # Random code

	return 0


def increaseEnergyBulletCharge(settings):
	settings.energy_frames_counter += 1

	if settings.energy_frames_counter % 10 == 0:
		settings.energy += 1
		settings.energy_frames_counter = 0


#####################
### Hitting block ###
#####################

def getShipPoint(ship, up, right):
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


def getBulletPoint(bullet, up):
	point = [0, 0]
	
	if up:
		point[0] = bullet.rect.centerx + 12
		point[1] = bullet.rect.centery + 5
	else:
		point[0] = bullet.rect.centerx + 12
		point[1] = bullet.rect.centery - 5

	return point


def spaceObjectHit(settings, screen, obj, ship):
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
	
	ship_point_coord = getShipPoint(ship, up, right)
	obj_center_coord = [obj.rect.x, obj.rect.y]
	#Вычисление расстояния от полученной точки до центра obj

	#координаты концов крыльев
	wing = [0, 0]
	if up == True:
		wing = top_wing = [ship.rect.x - 15, ship.rect.y + 40]
	else:
		wing = bottom_wing = [ship.rect.x - 15, ship.rect.y - 40]

	return checkSOSCollision(ship_point_coord, obj_center_coord, wing)


def perkHit(settings, perk):
	if perk.perk_type == 1:
		settings.ships_left += 1
	else:
		settings.energy += 50


def bulletHit(settings, screen, obj, bullet):
	if obj.rect.centery > bullet.rect.centery:#сверху
		up = True
	else:#снизу
		up = False

	bullet_point = getBulletPoint(bullet, up)
	obj_center_coord = [obj.rect.centerx, obj.rect.centery]
	
	return checkSOBCollision(bullet_point, obj_center_coord, screen)


######################
### Checking block ###
######################

def checkSpaceObjsEdges(settings, screen, spaceObjs):
	"""Граница вне экрана и удаление"""
	screen_rect = screen.get_rect()
	for obj in spaceObjs:#.copy():
		if obj.rect.right < screen_rect.left:
			spaceObjs.remove(obj)
			settings.total_obj -= 1


def checkPerkEdges(screen, perks):
	"""Граница вне экрана и удаление"""
	screen_rect = screen.get_rect()
	for perk in perks:#.copy():
		if perk.rect.right < screen_rect.left:
			perks.remove(perk)


def checkBulletEdges(screen, bullets):
	"""Граница вне экрана и удаление"""
	screen_rect = screen.get_rect()
	for bullet in bullets:#.copy():
		if bullet.rect.left > screen_rect.right:
			bullets.remove(bullet)


def checkSOSCollision(ship_point_coord, obj_center_coord, wing):
	"""Check SpaceObject-Ship collision"""
	#Пока радиус задаем перманентно но неявно(в формуле)
	#Ships body
	first_catet = abs(ship_point_coord[0] - obj_center_coord[0])
	second_catet = abs(ship_point_coord[1] - obj_center_coord[1])
	gipotinuza_body = (first_catet**2 + second_catet**2)**(0.5)
	
	#Ships wing
	first_wing_catet = abs(wing[0] - obj_center_coord[0])
	second_wing_catet = abs(wing[1] - obj_center_coord[1])
	gipotinuza_wing = (first_wing_catet**2 + second_wing_catet**2)**(0.5)
	
	if (gipotinuza_body - 38) < 0 or (gipotinuza_wing - 38) < 0:
		return True

	return False

from pygame import gfxdraw

def checkSOBCollision(bullet_point, obj_center_coord, screen):
	"""Check SpaceObject-Bullet collision"""
	first_catet = abs(bullet_point[0] - obj_center_coord[0])
	second_catet = abs(bullet_point[1] - obj_center_coord[1])
	gipotinuza = (first_catet**2 + second_catet**2)**(0.5)
    
	if (gipotinuza - 38) < 0:
		return True
		
	return False


######################
### Creating block ###
######################

def createSpaceObj(settings, screen, spaceObjs):
	"""Создает новый объект по некоторым условиям"""
	flag = True
	for obj in spaceObjs:
		if not obj.rect.x < settings.screen_width - int(1.2 * 80):
			flag = False

	if flag:
		seed(version=2)
		skin = randint(1,2)
		position = randint(-4, 3)
		amplitude = randint (30, 200)
		frequency = (randint(1, 15))
		traectory_num = randint(0, 1)
		speed_num = randint(0, 1 if frequency > 3 and traectory_num == 1 else len(settings.space_object_speed) - 1)	
		
		obj = SpaceObject(settings, screen, skin, position, speed_num, traectory_num, amplitude, frequency / 1000)

		settings.total_obj += 1
		spaceObjs.add(obj)


def createPerk(settings, screen, perk):
	seed(version=2)
	value = randint(0, 1000)
	if value == 200:
		skin = randint(0, 2)
		position = randint(-8, 7)

		new_perk = Perk(settings, screen, skin, position)
		perk.add(new_perk)


def createBullet(settings, ship, bullets):
	if settings.energy < 100:
		return

	seed(version=2)
	newBullet = Bullet(settings, ship)
	bullets.add(newBullet)
	settings.energy -= 100


def spawnObjects(settings, screen, spaceObjs, perk):
	"""Добавляет космический объект к группе"""
	createSpaceObj(settings, screen, spaceObjs)
	createPerk(settings, screen, perk)