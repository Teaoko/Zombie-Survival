import pygame, random, time
from Project.Settings import Settings

class Powerup(pygame.sprite.Sprite):
	def __init__(self, game, gui):
		super().__init__()
		self.groups = (game.bars)
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
        # Share settings from the game instance if available
        self.settings = getattr(game, 'settings', None) or Settings()
		self.boosters = self.settings.boosters
		self.gui = gui
		self.time_start = time.time()
		self.duration = 10
		self.bar_length = self.settings.bar_length
		self.x, self.y = self.settings.powerup_x, self.settings.powerup_y
		self.length = self.settings.bar_length
        self.powerup_img = pygame.Surface((130, 30), pygame.SRCALPHA).convert_alpha()
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
        # Choose a random booster and add a bar widget to GUI group
        power_names = [booster['name'] for booster in self.boosters]
        chosen_power = random.choice(power_names)
        if chosen_power not in self.PUL:
            self.PUL.append(chosen_power)
            # This sprite is already part of game.bars via groups setup
            if hasattr(self.gui, 'show_bars'):
                self.gui.show_bars()