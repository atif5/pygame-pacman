
from . import *
import random

def main():
    pass

def test():
    SCALE = 2
    FPS = 60
    screen = pygame.display.set_mode((224*SCALE, 288*SCALE))
    clock = pygame.time.Clock()
    pm = assets.PacMaze(scale=SCALE)
    p = actors.Pacman(pm, scale=SCALE)
    

    while True:
        pm.draw_on(screen, grids=False)
        p.draw_on(screen)
        p.displace()
        pygame.draw.rect(screen, assets.WHITE, p.next_rect(), width=1)
        if not p.velocity.any() or p.at_intersection():
            dirs = [0, 1, 2, 3]
            if p.dir_i < 1:
                invalid_dir = (not p.dir_i).real
            else:
                if p.dir_i == 2:
                    invalid_dir = 3
                else:
                    invalid_dir = 2
            p.turn(random.choice(dirs))
            print(p.dir_i)
        pygame.display.flip()
        clock.tick(FPS)



if __name__ == "__main__":
    test()
