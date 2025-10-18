import time
import pygame
from Project.Settings import Settings
from Project.resources import load_sound

# pygame.init() is handled in main


class Turret(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.settings = getattr(game, "settings", None) or Settings()

        # Movement/state
        self.vec = pygame.math.Vector2
        self.pos = self.vec((self.settings.turret_x, self.settings.turret_y))
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)
        self.ACC = 0.50
        self.FRIC = -0.20
        self.angle = 0
        self.turret_rotation_flag = False

        self.max_x = self.settings.max_x
        self.max_y = self.settings.max_y
        self.min_x = self.settings.min_x
        self.min_y = self.settings.min_y

        self.max_amo = self.settings.max_amo
        self.amo = self.settings.amo

        # Visuals
        self.turret_img = pygame.Surface((30, 40), pygame.SRCALPHA).convert_alpha()
        self._redraw_base()
        self.image = self.turret_img.copy()
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

        # Damage/flicker
        self.is_ethereal = False
        self.alpha = 255
        self.fade_speed = 100
        self.last_damage_time = 0
        self.damage_duration = 2

        # Sounds
        self.sound = load_sound("Turret hit.wav", 0.5)

    def _redraw_base(self) -> None:
        self.turret_img.fill((0, 0, 0, 0))
        # Body
        pygame.draw.circle(self.turret_img, "white", (15, 28), 10)
        # Barrel (drawn within surface bounds so it is visible)
        pygame.draw.rect(self.turret_img, "white", (13, 2, 4, 22))

    def handle_rotate(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t] and not self.turret_rotation_flag:
            self.TurretRotate(180)
            self.turret_rotation_flag = True
        elif not keys[pygame.K_t]:
            self.turret_rotation_flag = False

    def TurretMove(self) -> None:
        self.acc = self.vec(0, 0)
        self.handle_rotate()

        keys = pygame.key.get_pressed()
        self.acc.x += (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.acc.y += (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

        self.acc.x += self.vel.x * self.FRIC
        self.acc.y += self.vel.y * self.FRIC

        self.vel += self.acc
        self.pos += self.vel + self.acc

        self.pos.x = max(self.min_x, min(self.pos.x, self.max_x))
        self.pos.y = max(self.min_y, min(self.pos.y, self.max_y))

        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

        for zombie in list(self.game.zombieList.sprites()):
            if self.rect.colliderect(zombie.rect) and not self.is_ethereal and not zombie.is_dead:
                self.update_ethereal()
                self.is_ethereal = True
                self.game.lives -= 1
                zombie.kill()
                self.last_damage_time = time.time()
                self.sound.play()

        if self.is_ethereal:
            self.flicker()

    def update_ethereal(self) -> None:
        self.image.set_alpha(self.alpha)

    def flicker(self) -> None:
        current_time = time.time()
        if current_time - self.last_damage_time <= self.damage_duration:
            alpha_ratio = (current_time - self.last_damage_time) / self.damage_duration
            self.alpha = 255 - int(alpha_ratio * 255)
            self.image.set_alpha(self.alpha)
        else:
            self.is_ethereal = False
            self.alpha = 255
            self.image.set_alpha(self.alpha)

    def TurretRotate(self, angle: float) -> None:
        self.angle = (self.angle + angle) % 360
        rotated_image = pygame.transform.rotozoom(self.turret_img, self.angle, 1)
        self.image = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA).convert_alpha()
        self.image.blit(rotated_image, (0, 0))
        self.rect = self.image.get_rect(center=self.rect.center)
