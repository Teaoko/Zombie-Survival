import pygame
from pygame.locals import *
from Project.Settings import Settings
from Project.Zombie import Zombie
import time

pygame.init()

class Turret(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.settings = Settings()
		self.zombie = Zombie(1, self)

		self.x, self.y = self.settings.turret_x, self.settings.turret_y
		self.r = self.settings.r
		self.max_x, self.max_y, self.min_x, self.min_y = self.settings.max_x, self.settings.max_y, self.settings.min_x, self.settings.min_y

		self.ACC = 0.50
		self.FRIC = -0.20
		self.vec = pygame.math.Vector2
		self.pos = self.vec((200, 200))
		self.vel = self.vec(0,0)
		self.acc = self.vec(0,0)
		self.angle = 0
		self.angle_speed = 0
		self.toggle_rotating = False
		self.old_pos = self.pos

		self.max_amo = self.settings.max_amo
		self.amo = self.settings.amo
		self.angle = 0
		self.turret_img = pygame.Surface((30, 30), pygame.SRCALPHA)
		self.image = self.turret_img
		self.turret = pygame.draw.circle(self.turret_img, ("white"), (15, 15), 10)
		self.turret = pygame.draw.rect(self.turret_img, ("white"), (8, -55, 14, 70))
		self.rect = self.image.get_rect(center = (self.x, self.y))
		self.is_ethereal = False
		self.alpha = 255
		self.fade_speed = 100 
		self.last_damage_time = 0
		self.damage_duration = 2

		self.sound = pygame.mixer.Sound("Sounds/Turret hit.wav")
		self.sound.set_volume(0.5) 

	def handle_rotate(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_t] and not self.turret_rotation_flag:
			self.TurretRotate(180)
			self.turret_rotation_flag = True
		elif not keys[pygame.K_t]:
			self.turret_rotation_flag = False
	
	def TurretMove(self):
		self.acc = self.vec(0,0)
		self.handle_rotate()
		
		keys = pygame.key.get_pressed()
		self.acc.x += (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]) 
		self.acc.y += (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w]) 
		
		self.pos.x = max(self.min_x, min(self.pos.x, self.max_x))
		self.pos.y = max(self.min_y, min(self.pos.y, self.max_y)) 
		self.acc.x += self.vel.x * self.FRIC
		self.acc.y += self.vel.y * self.FRIC
		
		self.vel += self.acc
		self.pos += self.vel + self.acc

		self.rect.centerx = int(self.pos.x)
		self.rect.centery = int(self.pos.y)

		for zombie in self.game.zombieList.sprites():
			if self.rect.colliderect(zombie.rect) and not self.is_ethereal and not zombie.is_dead:
				self.update_ethereal()
				self.is_ethereal = True
				self.game.lives -= 1
				self.game.zombieList.remove(zombie)
				self.last_damage_time = time.time()
				pygame.mixer.music.load("Sounds/Turret hit.wav")
				pygame.mixer.music.play()

		if self.is_ethereal:
			self.flicker()

	def update_ethereal(self):
		self.image.set_alpha(self.alpha)

	def flicker(self):
		current_time = time.time()
		if current_time - self.last_damage_time <= self.damage_duration:
			alpha_ratio = (current_time - self.last_damage_time) / self.damage_duration
			self.alpha = 255 - int(alpha_ratio * 255)
			self.image.set_alpha(self.alpha)
		else:
			self.is_ethereal = False
			self.alpha = 255
			self.image.set_alpha(self.alpha)

	def TurretRotate(self, angle):
		self.angle += angle
		rotated_image = pygame.transform.rotozoom(self.turret_img, self.angle, 1)
		self.image = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
		self.image.blit(rotated_image, (0, 0))
		self.rect = self.image.get_rect(center=self.rect.center)