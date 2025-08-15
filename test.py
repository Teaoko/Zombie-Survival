import pygame, sys

pygame.init()

width, height = 500, 500

info = pygame.display.Info()
monitor_width, monitor_height = info.current_w, info.current_h
screen = pygame.display.set_mode((monitor_width, monitor_height), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Test")

design_width, design_height = width, height 
game_surface = pygame.Surface((design_width, design_height))

def get_quit():
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
			running = False
			pygame.quit()
			sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    get_quit()
    game_surface.fill((255, 255, 255))
    pygame.draw.rect(game_surface, (0, 255, 0), (design_width//2, design_height//2, 25, 50))
    scaled_surface = pygame.transform.scale(game_surface, (monitor_width, monitor_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.update()