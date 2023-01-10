
from . import *

def main():
    pass

def test():
    SCALE = 4
    screen = pygame.display.set_mode((224*SCALE, 288*SCALE))
    clock = pygame.time.Clock()
    pm = assets.PacMaze(scale=SCALE)
    p = actors.Pacman(pm, scale=SCALE)
    

    while True:
        pm.draw_on(screen, grids=False)
        p.draw_on(screen)
        p.displace()
        pygame.draw.rect(screen, "#ff0000", p.current_tile(), width=1)
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    test()
