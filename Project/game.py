import pygame, time, sys
from Project.resources import load_sound

from Project.Zombie import Zombie
from Project.Bullet import Bullet
from Project.gui import GUI
from Project.Settings import Settings


class Game:
    def __init__(self, db):
        from Project.Turret import Turret
        self.game_state = "menu"
        # Hold a single Settings instance shared across objects
        self.settings = Settings()
        self.length = self.settings.bar_length
        self.bars = pygame.sprite.Group()
        self.db = db

        # Fullscreen at desktop resolution; draw to a logical design surface and letterbox
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Zombie Survival")
        self.monitor_width, self.monitor_height = self.display.get_size()
        self.design_width, self.design_height = self.settings.width, self.settings.height
        self.screen = pygame.Surface((self.design_width, self.design_height)).convert_alpha()
        self._compute_scaler()

        self.turret = Turret(self)
        # Do not create a zombie here; spawns are managed by zombieSpawn
        self.gui = GUI(self, self.db)

        self.delta_x = self.settings.delta_x
        self.delta_y = self.settings.delta_y
        self.clock = pygame.time.Clock()
        self.zombie_time_count = self.settings.zombie_time_count
        self.ethereal_time_count = self.settings.ethereal_time_count

        self.zombieList = pygame.sprite.Group()
        self.bulletList = pygame.sprite.Group()
        self.turretList = pygame.sprite.Group()

        self.spawn = False
        self.zombieKill = False
        self.can_damage = False
        self.spawnTime = self.settings.spawnTime
        self.game_state = self.settings.game_state
        self.velX = self.settings.velX
        self.velY = self.settings.velY
        self.start_game = self.settings.start_game
        self.start_wave = self.settings.start_wave
        self.wave = self.settings.wave
        self.hit_wave = self.settings.hit_wave
        self.dollars = self.settings.dollars
        self.hits = self.settings.hits
        self.hits_needed = self.settings.hits_needed
        self.needs_reload = "no"

        self.start_time = time.time()

        self.got_powerup = False
        self.last_print = 0
        self.last_count = 0
        self.print_delay = 4
        self.fade_counter = 0

        self.lives = self.settings.lives
        self.life_added = self.settings.life_added

        # Sounds
        self.snd_fire = load_sound("Turret fired.wav", 0.5)
        self.snd_reload = load_sound("Turret reload.wav", 0.5)
        self.snd_cant = load_sound("Can't reload.wav", 0.5)

        # Joystick info (optional init)
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

    def BulletMove(self, bullet: Bullet) -> None:
        # Remove bullet if it leaves bounds vertically
        if bullet.rect.y <= 0 or bullet.rect.y >= 400:
            bullet.kill()
            return

        bullet.update()

        bullets_to_remove = []
        for zombie in self.zombieList.sprites():
            if bullet.rect.colliderect(zombie.rect) and not zombie.is_dead:
                self.hits += 1
                self.dollars += 1
                if not self.life_added and self.hits >= self.hits_needed:
                    self.lives += 1
                    self.life_added = True
                    self.hits_needed += 200
                zombie.current_health -= self.settings.bullet_damage
                bullets_to_remove.append(bullet)

        for b in bullets_to_remove:
            b.kill()

        self.life_added = False

    def handleBullets(self, event) -> None:
        # Joystick events
        if event.type == pygame.JOYBUTTONDOWN:
            # Button 0 to shoot
            if event.button == 0:
                if self.turret.amo > 0 and len(self.bulletList) < 3:
                    self.turret.amo -= 1
                    self.bulletList.add(Bullet(self.turret.rect.centerx, self.turret.rect.centery, self.turret))
                    self.snd_fire.play()
            # Button 1 to reload
            elif event.button == 1:
                if self.turret.amo < self.turret.max_amo:
                    self.turret.amo = self.turret.max_amo
                    self.snd_reload.play()
                else:
                    self.snd_cant.play()

        # Keyboard
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.turret.amo > 0 and len(self.bulletList) < 3:
                self.turret.amo -= 1
                self.bulletList.add(Bullet(self.turret.rect.centerx, self.turret.rect.centery, self.turret))
                self.snd_fire.play()
        if keys[pygame.K_r]:
            if self.turret.amo < self.turret.max_amo:
                self.turret.amo = self.turret.max_amo
                self.snd_reload.play()
            else:
                self.snd_cant.play()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            self.handleBullets(event)

    def zombieSpawn(self) -> None:
        # Spawn based on time count
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
            self.wave = 2
            self.zombieList.add(Zombie(2, self))
        else:
            self.zombieList.add(Zombie(1, self))

    def update_zombies(self) -> None:
        for zombie in self.zombieList.sprites():
            zombie.update_fade()

    def CountDown(self) -> None:
        # Increment every second while in-game; spawn on delay expiry
        if self.print_delay - (time.time() - self.last_print) >= 0 and self.game_state == "game":
            if time.time() - self.last_count > 1:
                self.last_count = time.time()
                self.zombie_time_count += 1
        else:
            self.zombieSpawn()
            self.last_print = time.time()

    def get_quit(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    def _compute_scaler(self) -> None:
        # Maintain aspect ratio, center with letterboxing
        scale_w = self.monitor_width / self.design_width
        scale_h = self.monitor_height / self.design_height
        self.scale = min(scale_w, scale_h)
        self.scaled_width = int(self.design_width * self.scale)
        self.scaled_height = int(self.design_height * self.scale)
        self.offset_x = (self.monitor_width - self.scaled_width) // 2
        self.offset_y = (self.monitor_height - self.scaled_height) // 2

    def to_design_pos(self, pos):
        px, py = pos
        # Transform from physical to design coordinates
        dx = (px - self.offset_x) / self.scale
        dy = (py - self.offset_y) / self.scale
        return (dx, dy)

    def present(self) -> None:
        # Scale logical surface to display with letterboxing
        scaled = pygame.transform.smoothscale(self.screen, (self.scaled_width, self.scaled_height))
        self.display.fill((0, 0, 0))
        self.display.blit(scaled, (self.offset_x, self.offset_y))
        pygame.display.flip()
