
from . import *

def main():
    pass

def test():
    SCALE = 2
    screen = pygame.display.set_mode((224*SCALE, 288*SCALE))
    clock = pygame.time.Clock()
    pm = assets.PacMaze(scale=SCALE)
    p = actors.Pacman(scale=SCALE)

    while True:
        pm.draw_on(screen, grids=False)
        p.draw_on(screen)
        p.displace()
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    test()
