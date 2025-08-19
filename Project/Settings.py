import random

class Settings:
	def __init__(self):
		#Position settings
		self.turret_x, self.turret_y = 200, 200
		self.powerup_x, self.powerup_y = 90, 120
		self.zombie_x, self.zombie_y = random.randrange(20, 385), 10

		#Bullet settings		
		self.bullet_damage = 1
		self.max_amo = 20
		self.amo = self.max_amo

		#Hitbox settings
		self.delta_x, self.delta_y = 2, 2
		self.velX, self.velY = 0, 0
		self.r = 14
		self.max_x, self.max_y = 385, 385
		self.min_x, self.min_y = 0 + self.r, 0 + self.r

		self.alpha = 420
		self.fade_speed = 2

		#Screen settings
		self.width, self.height = 400, 400
		self.game_state = "menu"

		#Time settings
		self.zombie_time_count, self.ethereal_time_count = 0, 0
		self.spawnTime = 2

		self.lives = 3
		self.bar_count = 5
		self.life_added = False
		
		#Powerup settings
		self.boosters = [
			{"name": 'Faster Bullet Speed', "time": 10, "speed": 0.8, "active": False},
			{"name": 'Faster Player Speed', "time": 4, "speed": 0.75, "active": False},
			{"name": 'More Bullets', "time": 10, "bullets_allowed": 8, "active": False},
			{"name": 'Invincible Damage', "time": 2, "bullets_damage": 10000, "active": False},
		]
		self.bar_length = 115
		
		#Value settings
		self.start_game, self.start_wave = False, True
		self.wave, self.hit_wave = 1, 1
		self.dollars, self.hits = 0, 0
		self.hits_needed = 200

		#Zombie settings
		self.zombie_ACC1 = 0.003
		self.zombie_ACC2 = 0.06
		self.zombie_ACC3 = 0.02
		self.zombie_ACC4 = 0.009
		self.zombie_ACC5 = 0.003

		self.zombie_colors = {
			'zombie1_color1': 'darkgreen',
			'zombie1_color2': 'black',
			'zombie2_color1': 'orangered',
			'zombie2_color2': 'black',
			'zombie3_color1': 'red1',
			'zombie3_color2': 'black',
			'zombie4_color1': 'springgreen',
			'zombie4_color2': 'white',
			'zombie5_color1': 'indigo',
			'zombie5_color2': 'gold',
		}

		self.zombie_isboss = {
			'zombie1': False,
			'zombie2': False,
			'zombie3': False,
			'zombie4': False,
			'zombie5': False,
		}

		self.zombie_health1, self.zombie_health2, self.zombie_health3 = 1, 3, 5
		self.zombie_health4, self.zombie_health5, self.zombie_health6 = 9, 25, 100

		self.zombie_data = {
		1: {'color1': self.zombie_colors['zombie1_color1'], 'color2': self.zombie_colors['zombie1_color2'],                
			'ACC': self.zombie_ACC1, 'size1': 12, 'size2': 3
		},
		2: {'color1': self.zombie_colors['zombie2_color1'], 'color2': self.zombie_colors['zombie2_color2'],
			'ACC': self.zombie_ACC2, 'size1': 12, 'size2': 3
		},
		3: {'color1': self.zombie_colors['zombie3_color1'], 'color2': self.zombie_colors['zombie3_color2'],
			'ACC': self.zombie_ACC3, 'size1': 12, 'size2': 8
		},
		4: {'color1': self.zombie_colors['zombie4_color1'], 'color2': self.zombie_colors['zombie4_color2'],
			'ACC': self.zombie_ACC4, 'size1': 12, 'size2': 10
		},
		5: {'color1': self.zombie_colors['zombie5_color1'], 'color2': self.zombie_colors['zombie5_color2'],
			'ACC': self.zombie_ACC5, 'size1': 12, 'size2': 9
		},
		#6: {'color1': self.zombie_colors['zombie6_color1'], 'color2': self.zombie_colors['zombie6_color2'],
			#'ACC': self.zombie_ACC6, 'size1': 12, 'size2': 14
		#},
	}