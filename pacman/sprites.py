
import pygame
from os import path

pygame.font.init()

BLACK = "#000000"
WHITE = "#ffffff"
YELLOW = "#ffff00"

root = path.join('.', __package__)

pacfont = pygame.font.Font(path.join(root, "fonts", "PAC-FONT.TTF"), 20)

spritesheet = pygame.image.load(path.join(root, "sprites", "pacmap.png"))
empty_maze = spritesheet.subsurface(pygame.Rect(228, 0, 224, 248))

char_sprites = spritesheet.subsurface(pygame.Rect(452, 0, 228, 248))
char_sprites.set_colorkey(BLACK)




