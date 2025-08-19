import pygame, time, sys, random
from pygame import locals
from pygame import mixer

from Project.Zombie import Zombie
from Project.Bullet import Bullet
from Project.gui import GUI
from Project.db import DB
from Project.Powerup import Powerup
from Project.Settings import Settings

pygame.init()
pygame.joystick.init()

class Game:
	def __init__(self, db):
		from Project.Turret import Turret 
		self.game_state = "menu"
		self.settings = Settings()
		self.length = self.settings.bar_length
		self.bars = pygame.sprite.Group()
		self.db = db 

		#Screen settings
		#Testing
		"""info = pygame.display.Info()
		self.monitor_width, self.monitor_height = info.current_w, info.current_h
		self.screen = pygame.display.set_mode((self.monitor_width, self.monitor_height), pygame.FULLSCREEN)
		pygame.display.set_caption("Zombie Survival")

		self.DESIGN_WIDTH, self.DESIGN_HEIGHT = 800, 600
		self.game_surface = pygame.Surface((self.DESIGN_WIDTH, self.DESIGN_HEIGHT))

		self.scaled_surface = pygame.transform.scale(self.game_surface, (self.monitor_width, self.monitor_height))
		#self.screen.blit(self.scaled_surface, (0, 0))"""

		self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
		pygame.display.set_caption("Zombie Survival")

		self.turret = Turret(self)
		self.zombie = Zombie(1, self)
		self.gui = GUI(self, self.db)
		#self.powerup = Powerup(self, self.gui)

		self.delta_x, self.delta_y = self.settings.delta_x, self.settings.delta_y
		self.clock = pygame.time.Clock()
		self.zombie_time_count, self.ethereal_time_count = self.settings.zombie_time_count, self.settings.ethereal_time_count
		#Screen settings

		self.zombieList, self.bulletList, self.turretList = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

		self.spawn, self.zombieKill = False, False
		self.can_damage = False
		self.spawnTime = self.settings.spawnTime
		self.game_state = self.settings.game_state
		self.velX, self.velY = self.settings.velX, self.settings.velY
		self.start_game = self.settings.start_game
		self.start_wave = self.settings.start_wave
		self.wave, self.hit_wave = self.settings.wave, self.settings.hit_wave
		self.dollars, self.hits = self.settings.dollars, self.settings.hits
		self.hits_needed = self.settings.hits_needed
		self.needs_reload = "no"

		self.start_time = time.time()

		self.got_powerup = False
		self.last_print, self.last_count, self.print_delay, self.fade_counter = 0, 0, 4, 0
		
		self.lives, self.settings.life_added = self.settings.lives, self.settings.life_added

		if pygame.joystick.get_count() == 0:
			print("No joystick connected.")
		else:
			joystick = pygame.joystick.Joystick(0)
			joystick.init()
			print(f"Detected joystick: {joystick.get_name()}")
			print(f"Buttons: {joystick.get_numbuttons()}")
			print(f"Axes: {joystick.get_numaxes()}")

	def BulletMove(self, bullet):
			self.zombieKill = False
			if bullet.x > bullet.max_x:
				bullet.x = bullet.max_x
			if bullet.x < bullet.min_x:
				bullet.x = bullet.min_x
			if bullet.y > bullet.max_y:
				bullet.y = bullet.max_y
			if bullet.y < bullet.min_y:
				bullet.y = bullet.min_y
			if bullet.rect.y <= 0:
				bullet.kill()
			elif bullet.rect.y >= 400:
				bullet.kill()
				
			bullet.update()
		
			self.bullets_to_remove = []
			for zombie in self.zombieList.sprites():
				if bullet.rect.colliderect(zombie.rect) and zombie.is_dead == False:
					self.hits += 1
					self.dollars += 1					
					if not self.life_added:
						if self.hits >= self.hits_needed:
							self.lives += 1
							self.life_added = True
							self.hits_needed += 200
					zombie.current_health -= self.settings.bullet_damage
					self.bullets_to_remove.append(bullet)

			for bullets in self.bullets_to_remove:
				bullet.kill()
				
			self.life_added = False

	#Testing
	"""def handleBullets(self, event):
		if pygame.joystick.get_count() == 0:
			print("No joystick connected!")
		else:
			# Initialize the first joystick
			joystick = pygame.joystick.Joystick(0)
			joystick.init()
			print(f"Joystick connected: {joystick.get_name()}")
		keys = pygame.key.get_pressed()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			if len(self.bulletList) >= 3 or self.turret.amo == 0:
				pass
		elif event.type == pygame.JOYBUTTONDOWN:
			if event.button == 0:
				self.turret.amo -= 1
				self.bulletList.add(Bullet(self.turret.rect.centerx, self.turret.rect.centery, self.turret))
			else: 
				self.turret.amo -= 1
				self.bulletList.add(Bullet(self.turret.rect.centerx, self.turret.rect.centery, self.turret))
				#sound_TF.play()
		if keys[pygame.K_r]:
			if self.turret.amo == self.turret.max_amo:
				pass
				#sound_CR.play()
			else:
				self.turret.amo = self.turret.max_amo
				#sound_TR.play()"""
	
	def handleBullets(self, event):
		# Check for joystick events
		if event.type == pygame.JOYBUTTONDOWN:
			# Button 0 (usually "A" on Xbox controllers) to shoot
			if event.button == 0:
				if self.turret.amo > 0 and len(self.bulletList) < 3:
					self.turret.amo -= 1
					self.bulletList.add(Bullet(self.turret.rect.centerx, self.turret.rect.centery, self.turret))
					# sound_TF.play()
			# Button 1 (usually "B") to reload
			elif event.button == 1:
				if self.turret.amo < self.turret.max_amo:
					self.turret.amo = self.turret.max_amo
					# sound_TR.play()
				else:
					# sound_CR.play()
					pass

		# Keyboard support (already present)
		keys = pygame.key.get_pressed()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			if self.turret.amo > 0 and len(self.bulletList) < 3:
				self.turret.amo -= 1
				self.bulletList.add(Bullet(self.turret.rect.centerx, self.turret.rect.centery, self.turret))
				# sound_TF.play()
		if keys[pygame.K_r]:
			if self.turret.amo < self.turret.max_amo:
				self.turret.amo = self.turret.max_amo
				# sound_TR.play()
			else:
				# sound_CR.play()
				pass

	def handle_events(self):
		for event in pygame.event.get():
			self.handleBullets(event)

	def zombieSpawn(self):
		#after these: 200, 220, 245, 260
		#Comments below r for testing
		if self.zombie_time_count >= 200:
			self.wave = 7
			self.zombieList.add(Zombie(6, self))
		elif self.zombie_time_count >= 130:
			self.wave = 6
			self.zombieList.add(Zombie(2, self))
		elif self.zombie_time_count >= 90:
			self.wave = 5
			self.zombieList.add(Zombie(5, self))
		elif self.zombie_time_count >= 55:
			self.wave = 4
			self.zombieList.add(Zombie(4, self))
		elif self.zombie_time_count >= 30:
			self.wave = 3
			self.zombieList.add(Zombie(3, self))
		elif self.zombie_time_count >= 12:
			#pygame.draw.rect(self.game_surface, (255, 255, 255), (self.DESIGN_WIDTH//2 - 25, self.DESIGN_HEIGHT//2 - 25, 50, 50))
			self.wave = 2
			self.zombieList.add(Zombie(2, self))
		elif self.zombie_time_count >= 0:
			self.zombieList.add(Zombie(1, self))
		#self.scaled_surface = pygame.transform.scale(self.game_surface, (self.monitor_width, self.monitor_height))
		#self.screen.blit(self.scaled_surface, (0, 0))

	def update_zombies(self):
		for zombie in self.zombieList.sprites():
			zombie.update_fade()

	def CountDown(self):
		#How Often It Executes
		if self.print_delay - (time.time() - self.last_print) >= 0 and self.game_state == "game":
			if time.time() - self.last_count > 1:
			#Time Delta From @start_time
				self.last_count = time.time()
				self.zombie_time_count += 1
			#Reset @last_print
		else:
			self.zombieSpawn()
			self.last_print = time.time()
		
	def get_quit(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
			self.running = False
			pygame.quit()
			sys.exit()