import pygame, sys
from pygame.locals import *
from pygame.sprite import Group
from Project.Bullet import Bullet
from Project.Zombie import Zombie
from Project.db import DB
from Project.Powerup import Powerup
from Project.Settings import Settings

pygame.init()

class GUI:
	def __init__(self, game, db):
		from Project.Turret import Turret
		self.game = game
		self.db = db
		self.settings = Settings()
		self.zombie = Zombie(1, self)
		self.turret = Turret(self.game)
		#self.powerup = Powerup(self.game, self)

		self.color_active = pygame.Color('lightskyblue3') 
		self.color_passive = pygame.Color('red') 
		self.color = self.color_passive
		self.active = False
		self.clock = pygame.time.Clock()

		self.font1, self.font2, self.font3, self.font4 = pygame.font.SysFont("Roboto", 40), pygame.font.SysFont("lucidasans", 55),  pygame.font.SysFont("corbel ", 55), pygame.font.SysFont("Roboto", 30)
		self.shop_upgrade_num = 0
		self.surf, self.surf_shop, self.upgrade_surf1 = self.font1.render("Shop", True, "black"), self.font2.render("X", True, "red"), self.font1.render("Faster Bullets", True, "black")
		self.button, self.shop_button, self.upgrade_button1 = pygame.Rect(140, 120, 100, 40), pygame.Rect(370, 0, 20, 20), pygame.Rect(200, 200, 40, 50)

		self.HSO = False
		self.PN = ''
		self.score_height = 10
		self.font5 = pygame.font.Font(None, 32)
		self.text_surface = self.font5.render("Please Enter a name: ", True, (255, 255, 255))
		self.done_typing, self.can_type = False, True
		self.lives = Group()

		self.sound_GO = pygame.mixer.Sound("Sounds/Game over.wav")
		self.sound_GO.set_volume(0.5) 

	def game_over_screen(self, game):
		self.sound_GO.play(0)
		pygame.mouse.set_visible(True)
		self.done_typing = False
		self.game.screen.fill((0, 0, 0))
		self.game.turret.amo = 20
		self.game.screen.blit(self.font1.render("Game Over", True, ("white")), [130, 30])
		self.game.screen.blit(self.font4.render("Press r to go back to the menu", True, ("white")), [60, 100])
		self.game.screen.blit(self.font4.render("Press esc to exit or stop the project", True, ("white")), [40, 140])

		if self.game.db.is_high_score(self.game.hits) and self.PNs_entered < self.PNs_allowed:
			self.can_type, self.HSO = True, False
			self.game.screen.blit(self.text_surface, (10, 350))
			self.text_surface = self.font5.render("Please Enter a name: ", True, (255, 255, 255))
			self.game.screen.blit(self.font5.render(self.PN, True, (255, 255, 255)), (10 + self.text_surface.get_width() + 5, 350))
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and self.can_type:
					if event.key == pygame.K_RETURN:
						self.game.db.insert_score(self.PN, self.game.hits)
						self.PNs_entered += 1
						self.can_type, self.done_typing = False, True
						event.unicode, self.PN = "", ""
						self.HSO = True
						break
					else:
						self.can_type = False
					if event.key == pygame.K_BACKSPACE:
						self.PN = self.PN[:-1]
					elif event.unicode.isalpha():
						self.PN += event.unicode

		else:
			self.text_surface = self.font5.render("", True, (255, 255, 255))
			self.game.screen.blit(self.text_surface, (10, 300))
			self.PN = ""
			self.HSO, self.can_type = False, False

		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if keys[pygame.K_r]:
				self.game.game_state = "menu"
				self.done_typing = False
				self.menu_screen(self.game)
				break
			elif keys[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()

		self.show_HS(self.game)
		self.game.get_quit()
		self.clock.tick(60)
		pygame.display.flip()

	def show_HS(self, game):
		self.game.get_quit()
		self.scores = self.game.db.get_top_scores(5)
		self.score_height = 200
		for score_tuple in self.scores:
			score, name = score_tuple[0], score_tuple[1]
			score_text = f"{score} - {name}"
			score_msg = self.font1.render(score_text, True, (255, 255, 255))
			self.game.screen.blit(score_msg, [170, self.score_height])
			self.score_height += 27

	def show_lives(self, game):
		self.x_offset, self.y_offset = 5, 370

		self.turret_surf = self.game.turret.image
		"""Calculates the width of each one, and to ensure that even if there are no none, the
		surface has a non-zero width, and the if makes sure that it stays at least 1 pixel"""
		self.ats = pygame.Surface(((self.game.lives * (self.turret_surf.get_width() + 5)) + 1, self.turret_surf.get_height())) if self.game.lives > 0 else pygame.Surface((1, self.turret_surf.get_height()))#pygame does not accept a width of 0
		self.ats.set_colorkey((0, 0, 0, 0))#all turret surfaces
		
		for live_number in range(self.game.lives):
			self.x_pos = live_number * (self.turret_surf.get_width() + 5)
			self.ats.blit(self.turret_surf, (self.x_pos, 0))
		
		self.game.screen.blit(self.ats, (self.x_offset, self.y_offset))

	def show_bars(self):
		self.x_offset, self.y_offset = 5, 100
		self.aps = pygame.Surface((130,200), pygame.SRCALPHA)
		self.aps.set_colorkey((0, 0, 0, 0))#all powerup surfaces

		for i, powerup in enumerate(self.game.bars):
			powerup.PUCountDown()
			self.aps.blit(powerup.powerup_img, (10, 10 + (powerup.offset * i)))
			
		self.game.screen.blit(self.aps, (self.x_offset, self.y_offset))
	
	def menu_screen(self, game):
		self.game.get_quit()
		pygame.mouse.set_visible(True)
		self.game.start_wave, self.game.game_over = True, False
		self.game.wave, self.game.hits = 1, 0
		self.game.dollars += self.game.hits
		self.game.zombie_time_count = 0
		self.PNs_entered, self.PNs_allowed = 0, 1
		self.game.lives = 3
		self.game.bars = pygame.sprite.Group()
		self.game.zombieList.empty()
		self.game.bulletList.empty()
		self.game.game_over = False
		self.game.screen.fill(("white"))
		self.a, self.b = pygame.mouse.get_pos()
		self.game.screen.blit(self.font1.render("Press space to begin", True, ("black")), [60, 180])
		if self.button.x <= self.a <= self.button.x + 100 and self.button.y <= self.b <= self.button.y + 40:
			pygame.draw.rect(self.game.screen, ("gray27"), self.button)
			self.game.screen.blit(self.surf, (self.button.centerx - 35, self.button.centery - 15))
		else:
			pygame.draw.rect(self.game.screen, ("gray39"), self.button)
			self.game.screen.blit(self.surf, (self.button.centerx - 35, self.button.centery - 15))
		self.clock.tick(60)
		pygame.display.update()

	def shop_screen(self, game):
		self.game.get_quit()
		pygame.mouse.set_visible(True)
		self.c, self.d = pygame.mouse.get_pos()
		self.game.screen.fill(("sienna"))
		self.game.screen.blit(self.surf_shop, (self.shop_button.centerx - 10, self.shop_button.centery-15))
		self.clock.tick(60)
		pygame.display.update()

	def game_screen(self, game):
		self.game.get_quit()
		pygame.mouse.set_visible(False)
		self.game.screen.fill(("gray43"))
		self.game.handle_events()
		self.game.screen.blit(self.font1.render("amo: " + str(self.game.turret.amo), True, ("black")), [270, 360])
		self.game.screen.blit(self.font2.render("money: " + str(self.game.dollars), True, ("black")), [0, 0])
		self.game.screen.blit(self.font3.render("wave: " + str(self.game.wave), True, ("black")), [0, 50])
		self.game.CountDown()
		self.game.turret.TurretMove()
		self.game.screen.blit(self.game.turret.image, self.game.turret.rect) 
		for zombie in self.game.zombieList.sprites():
			self.zombie.image.set_alpha(zombie.alpha)
			self.game.screen.blit(zombie.image, zombie.rect)
			zombie.ZombieMove(self.game.screen)
		for bullet in self.game.bulletList:
			self.game.screen.blit(bullet.image, bullet.rect)
			self.game.BulletMove(bullet)
		self.game.update_zombies()
		self.show_lives(self.game)
		self.show_bars()
		self.clock.tick(60)
		pygame.display.update()