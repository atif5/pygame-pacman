
import pygame
import time

pygame.font.init()

font = pygame.font.Font("./ARCADE_N.TTF", 15)
text = font.render("HIGH SCORE", True,  "#FFFFFF")
ghost = font.render("9", True,  "#FF0000")

screen = pygame.display.set_mode((500, 500))

while True:
    screen.blit(text, (100, 100))
    screen.blit(ghost, (50, 100))
    pygame.display.flip()
    time.sleep(1)
