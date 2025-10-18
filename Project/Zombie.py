import pygame, random, pygame.sprite
from Project.Settings import Settings
from Project.Powerup import Powerup
from Project.resources import load_sound

# pygame.init() is handled in main

class Zombie(pygame.sprite.Sprite):
	def __init__(self, zombie_type, game):
		super().__init__()
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.powerup = None
    # Share settings from the parent game to avoid repeated instantiation
    self.settings = getattr(game, 'settings', None) or Settings()
		self.r = self.settings.r
		self.max_x, self.max_y, self.min_x, self.min_y = self.settings.max_x, self.settings.max_y, self.settings.min_x, self.settings.min_y
		self.alpha = self.settings.alpha
		self.fade_speed = self.settings.fade_speed

		self.zombie_type = zombie_type
		if self.zombie_type == 1:
			self.zombie_health = 1

		elif self.zombie_type == 2:
			self.zombie_health = 3

		elif self.zombie_type == 3:
			self.zombie_health = 5

		elif self.zombie_type == 4:
			self.zombie_health = 9

		elif self.zombie_type == 5:
			self.zombie_health = 25
		
		elif self.zombie_type == 6:
			self.zombie_health = 100

		self.zombie_data = self.settings.zombie_data
		self.zombie_info = self.settings.zombie_data.get(self.zombie_type)
		self.zombie_isboss = self.settings.zombie_isboss

		self.health_start = self.zombie_health
		self.current_health = self.health_start
		self.is_dead = False
		self.x, self.y = self.settings.zombie_x, self.settings.zombie_y

		self.FRIC = -0.20
		self.vec = pygame.math.Vector2
		self.pos = self.vec((self.x, self.y))
		self.vel = self.vec(0,0)
		self.acc = self.vec(0,0)
		self.max_x = 385
		self.max_y = 385
		self.min_x = 0 + self.r
		self.min_y = 0 + self.r
		self.dy = self.zombie_type

        # Prepare surface once and reuse; convert_alpha for faster blits
        is_boss = self.settings.zombie_isboss.get(f"zombie{self.zombie_type}", False)
        base_size = (30, 30) if is_boss else (30, 30)
        # Ensure consistent size and center point for drawing
        zombie_img = pygame.Surface(base_size, pygame.SRCALPHA).convert_alpha()
        self.image = zombie_img

		self.alpha = 255
		self.fade_speed = 2

    self.sound = load_sound("Zombie hit.wav", 0.5)

        if self.zombie_info:
            center = (zombie_img.get_width() // 2, zombie_img.get_height() // 2)
            pygame.draw.circle(zombie_img, self.zombie_info['color1'], center, self.zombie_info['size1'])
            pygame.draw.circle(zombie_img, self.zombie_info['color2'], center, self.zombie_info['size2'])
            self.ACC = self.zombie_info['ACC']

		self.rect = self.image.get_rect(center=(self.x, self.y))

	def draw_healthBar(self, screen):
		pygame.draw.rect(screen, "red", (self.rect.centerx - 12, (self.rect.centery + 13), self.rect.width, 15))
		if self.current_health > 20:
			pygame.draw.rect(screen, "orange", (self.rect.centerx - 12, (self.rect.centery + 13), int(self.rect.width * (self.current_health / self.health_start)), 15))
		elif self.current_health > 12:
			pygame.draw.rect(screen, "gold2", (self.rect.centerx - 12, (self.rect.centery + 13), int(self.rect.width * (self.current_health / self.health_start)), 15))
		elif self.current_health > 5:
			pygame.draw.rect(screen, "yellow", (self.rect.centerx - 12, (self.rect.centery + 13), int(self.rect.width * (self.current_health / self.health_start)), 15))
		elif self.current_health > 0:
			pygame.draw.rect(screen, "green", (self.rect.centerx - 12, (self.rect.centery + 13), int(self.rect.width * (self.current_health / self.health_start)), 15))

	def ZombieMove(self, screen):
		self.draw_healthBar(screen)
		if self.x > self.max_x: 
			self.x = self.max_x
		if self.x < self.min_x:
			self.x = self.min_x
        if self.pos.y > self.max_y:
            self.pos.y = self.max_y
            self.kill()
            self.game.lives = max(0, self.game.lives - 1)
		if self.y < self.min_y:
			self.y = self.min_y
		if self.game.lives <= 0:
			self.game.game_over = True
			self.game.game_state = "game_over"

		self.pos.x = max(self.min_x, min(self.pos.x, self.max_x))
		self.pos.y = max(self.min_y, min(self.pos.y, self.max_y))
		self.acc.y = self.ACC
		self.acc.x += self.vel.x * self.FRIC
		self.acc.y += self.vel.y * self.FRIC
		self.vel += self.acc

		self.pos += self.vel + 2.0 * self.acc
		self.rect.centerx = int(self.pos.x)
		self.rect.centery = int(self.pos.y)

	def update_fade(self):
		if self.current_health <= 0:
			self.is_dead = True
			self.fade_out()
		else:
            self.image.set_alpha(self.alpha)

	def fade_out(self):
		self.alpha -= self.fade_speed
		if self.alpha <= 0:
			self.sound.play(0)
			self.kill()
			self.PUC = random.randint(1, 100)#Power-up chance
			if self.PUC % 7 == 0:
				self.powerup = Powerup(self.game, self)
				self.powerup.collect_powerup(self)
			else:
				pass
		else:
			self.image.set_alpha(self.alpha)