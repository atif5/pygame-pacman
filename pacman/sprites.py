
import pygame

spritesheet = pygame.image.load("./pacman/sprites/pacmap.png")
empty_maze = spritesheet.subsurface(pygame.Rect(228, 0, 224, 248))
char_sprites = spritesheet.subsurface(pygame.Rect(452, 0, 228, 248))


def test():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((228, 248))
    screen.blit(char_sprites, (0, 0))
    screen.set_at((21, 65), "#00ff00")
    while True:
        pygame.display.flip()
        clock.tick(1)


if __name__ == "__main__":
    test()

