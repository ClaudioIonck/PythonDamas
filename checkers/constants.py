import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (139, 69, 19) #Vai ser marrom escuro
WHITE = (255, 255, 255) 
BLACK = (245, 222, 179) # Vai ser Marrom claro
BLUE = (124, 252, 0) # Vai ser o Green
GREY = (0, 0, 0) # Vai ser o BLACK


CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
