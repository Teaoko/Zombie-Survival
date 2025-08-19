import pygame, math
from Project.Settings import Settings

class Bullet(pygame.sprite.Sprite):
	def __init__(self, startX, startY, turret):
		super().__init__()
		pygame.sprite.Sprite.__init__(self)

		self.turret = turret
		self.settings = Settings()

		self.x, self.y = self.turret.rect.x, self.turret.rect.y
		self.r = self.settings.r
		self.max_x, self.max_y, self.min_x, self.min_y = self.settings.max_x, self.settings.max_y, self.settings.min_x, self.settings.min_y
		
		self.speed = 5

		self.image = pygame.Surface((30, 50), pygame.SRCALPHA)
		pygame.draw.rect(self.image, (255, 215, 0, 255), (10, -8, 10, 20))

		self.rect = self.image.get_rect(center=(startX, startY))
		self.init_dir()

	def init_dir(self):
		angle_rad = math.radians(self.turret.angle)
		start_x = self.turret.rect.centerx
		start_y = self.turret.rect.centery 
		self.rect.center = (start_x, start_y)
		self.vel = pygame.math.Vector2(math.sin(angle_rad) * self.speed, -math.cos(angle_rad) * self.speed)

	def update(self):
		self.rect.x += self.vel.x
		self.rect.y += self.vel.y