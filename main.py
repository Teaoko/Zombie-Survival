import pygame, sys, time, sqlite3
from pygame import locals
from Project.Turret import Turret
from Project.Zombie import Zombie
from Project.Bullet import Bullet
from Project.gui import GUI
from Project.game import Game
from Project.db import DB
from Project.Settings import Settings
from random import randint
#color codes snow3(205, 201 201, 255)  gold(255, 215, 0, 255) peru(205, 133, 63, 255), purple 4(85, 26, 139, 255), saddlebrown(139, 69, 19, 255), salmon4(139, 76, 57, 255)
#Book

pygame.init()	
db = DB()
game = Game(db)
settings = Settings() 

"""turret = Turret(game)
gui = GUI(game, db)"""

sound_TF = pygame.mixer.Sound("Sounds/Turret fired.wav")
sound_TF.set_volume(0.5) 
sound_TR = pygame.mixer.Sound("Sounds/Turret reload.wav")
sound_TR.set_volume(0.5) 
sound_CR = pygame.mixer.Sound("Sounds/Can't reload.wav")
sound_CR.set_volume(0.5)

while True:
	if game.game_state == "menu":
		game.gui.menu_screen(game)
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				game.game_state = "game"
			if event.type == pygame.MOUSEBUTTONDOWN:
				if game.gui.button.collidepoint(event.pos):
					game.game_state = "shop"

	if game.game_state == "shop":
		game.gui.shop_screen(game)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if game.gui.shop_button.collidepoint(event.pos):
						game.game_state = "menu"

	if game.game_state == "game":
		while game.game_state == "game":
			game.gui.game_screen(game)

	if game.game_state == "game_over": 
		while game.game_state == "game_over":
			game.gui.game_over_screen(game) 