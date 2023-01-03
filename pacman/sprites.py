
import pygame

spritesheet = pygame.image.load("./pacman/sprites/pacmap.png")
empty_maze = spritesheet.subsurface(pygame.Rect(228, 0, 224, 248))
char_sprites = spritesheet.subsurface(pygame.Rect(452, 0, 228, 248))