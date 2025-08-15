import pygame, sys, random, math, time
from pygame.locals import QUIT
from Project.Settings import Settings

class Powerup(pygame.sprite.Sprite):
	def __init__(self, game, gui):
		super().__init__()
		self.groups = (game.bars)
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.settings = Settings()
		self.boosters = self.settings.boosters
		self.gui = gui
		self.time_start = time.time()
		self.duration = 10
		self.bar_length = self.settings.bar_length
		self.x, self.y = self.settings.powerup_x, self.settings.powerup_y
		self.length = self.settings.bar_length
		self.powerup_img = pygame.Surface((130, 30), pygame.SRCALPHA)
		self.bar_fill = pygame.draw.rect(self.powerup_img, ("blue"), (5, 5, self.length, 10))
		self.BFR = pygame.draw.rect(self.powerup_img, ("gray1"), (0, 0, 120, 20), border_radius = 5) #Bar fill radius
		self.rect = self.powerup_img.get_rect(center=(self.x, self.y))
		self.PUL = [] #Power up list
		self.offset = 50

	def PUCountDown(self):
		self.powerup_img.fill((pygame.SRCALPHA))
		self.time_elapsed = time.time() - self.time_start
		self.length = 110 * (1 - (self.time_elapsed / self.duration))
		self.BFR = pygame.draw.rect(self.powerup_img, ("gray1"), (0, 0, 120, 20), 2)
		self.bar_fill = pygame.draw.rect(self.powerup_img, "blue", (5, 5, self.length, 10))
		if self.time_elapsed >= self.duration:
			self.kill()

	def collect_powerup(self, gui):
		self.PPN = [booster['name'] for booster in self.boosters]  # Pick power name
		self.PT = [time['time'] for time in self.boosters]  # Power time
		self.ATP = [active['active'] for active in self.boosters]  # Active power times
		self.PUN = random.choice(self.PPN)  # Power up name
		if self.PUN not in self.PUL and isinstance(self.game.bars, int):
			self.game.bars += 1
			self.PUL.append(self.PUN)
			self.gui.show_bars()
		else:  # no power-ups in the list
			pass